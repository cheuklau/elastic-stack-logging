# frozen_string_literal: false
#--
# = Ruby-space definitions that completes C-space funcs for X509 and subclasses
#
# = Info
# 'OpenSSL for Ruby 2' project
# Copyright (C) 2002  Michal Rokos <m.rokos@sh.cvut.cz>
# All rights reserved.
#
# = Licence
# This program is licensed under the same licence as Ruby.
# (See the file 'LICENCE'.)
#++

module OpenSSL
  module X509
    class Name
      module RFC2253DN
        Special = ',=+<>#;'
        HexChar = /[0-9a-fA-F]/
        HexPair = /#{HexChar}#{HexChar}/
        HexString = /#{HexPair}+/
        Pair = /\\(?:[#{Special}]|\\|"|#{HexPair})/
        StringChar = /[^\\"#{Special}]/
        QuoteChar = /[^\\"]/
        AttributeType = /[a-zA-Z][0-9a-zA-Z]*|[0-9]+(?:\.[0-9]+)*/
        AttributeValue = /
          (?!["#])((?:#{StringChar}|#{Pair})*)|
          \#(#{HexString})|
          "((?:#{QuoteChar}|#{Pair})*)"
        /x
        TypeAndValue = /\A(#{AttributeType})=#{AttributeValue}/

        module_function

        def expand_pair(str)
          return nil unless str
          return str.gsub(Pair){
            pair = $&
            case pair.size
            when 2 then pair[1,1]
            when 3 then Integer("0x#{pair[1,2]}").chr
            else raise OpenSSL::X509::NameError, "invalid pair: #{str}"
            end
          }
        end

        def expand_hexstring(str)
          return nil unless str
          der = str.gsub(HexPair){$&.to_i(16).chr }
          a1 = OpenSSL::ASN1.decode(der)
          return a1.value, a1.tag
        end

        def expand_value(str1, str2, str3)
          value = expand_pair(str1)
          value, tag = expand_hexstring(str2) unless value
          value = expand_pair(str3) unless value
          return value, tag
        end

        def scan(dn)
          str = dn
          ary = []
          while true
            if md = TypeAndValue.match(str)
              remain = md.post_match
              type = md[1]
              value, tag = expand_value(md[2], md[3], md[4]) rescue nil
              if value
                type_and_value = [type, value]
                type_and_value.push(tag) if tag
                ary.unshift(type_and_value)
                if remain.length > 2 && remain[0] == ?,
                  str = remain[1..-1]
                  next
                elsif remain.length > 2 && remain[0] == ?+
                  raise OpenSSL::X509::NameError,
                    "multi-valued RDN is not supported: #{dn}"
                elsif remain.empty?
                  break
                end
              end
            end
            msg_dn = dn[0, dn.length - str.length] + " =>" + str
            raise OpenSSL::X509::NameError, "malformed RDN: #{msg_dn}"
          end
          return ary
        end
      end

      class << self
        def parse_rfc2253(str, template=OBJECT_TYPE_TEMPLATE)
          ary = OpenSSL::X509::Name::RFC2253DN.scan(str)
          self.new(ary, template)
        end

        def parse_openssl(str, template=OBJECT_TYPE_TEMPLATE)
          if str.start_with?("/")
            # /A=B/C=D format
            ary = str[1..-1].split("/").map { |i| i.split("=", 2) }
          else
            # Comma-separated
            ary = str.split(",").map { |i| i.strip.split("=", 2) }
          end
          self.new(ary, template)
        end

        alias parse parse_openssl
      end

      def pretty_print(q)
        q.object_group(self) {
          q.text ' '
          q.text to_s(OpenSSL::X509::Name::RFC2253)
        }
      end
    end

    class StoreContext
      def cleanup
        warn "(#{caller.first}) OpenSSL::X509::StoreContext#cleanup is deprecated with no replacement" if $VERBOSE
      end
    end

    class Certificate
      def pretty_print(q)
        q.object_group(self) {
          q.breakable
          q.text 'subject='; q.pp self.subject; q.text ','; q.breakable
          q.text 'issuer='; q.pp self.issuer; q.text ','; q.breakable
          q.text 'serial='; q.pp self.serial; q.text ','; q.breakable
          q.text 'not_before='; q.pp self.not_before; q.text ','; q.breakable
          q.text 'not_after='; q.pp self.not_after
        }
      end
    end
  end
end
