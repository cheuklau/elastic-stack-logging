require_relative "spec_helper"

describe "constant_sql_override extension" do
  before do
    @db = Sequel.mock.extension(:constant_sql_override)
  end

  it 'overrides configured constants' do
    @db.set_constant_sql(Sequel::CURRENT_TIMESTAMP, "CURRENT TIMESTAMP AT TIME ZONE 'UTC'")
    @db[:tbl].where(foo: Sequel::CURRENT_TIMESTAMP).first
    @db.sqls.must_equal ["SELECT * FROM tbl WHERE (foo = CURRENT TIMESTAMP AT TIME ZONE 'UTC') LIMIT 1"]
  end

  it 'freezes the constant_sqls hash' do
    @db.freeze
    @db.constant_sqls.frozen?.must_equal true
  end
end
