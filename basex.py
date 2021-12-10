from pathlib import Path
import os
import pprint
from BaseXClient import BaseXClient

# セッション作成
session = BaseXClient.Session('test-host', 1984, 'admin', 'admin')

try:
    # DBオープン
    session.execute("open case")
    print(session.info())

    # DBの内容を表示
    print("\n" + session.execute("xquery //entry[@headword='綺麗だ/きれいだ']/caseframe/argument[contains(@case,'ガ格')]/component"))
    print("正常終了しました\n")

finally:
    # セッションを閉じる
    if session:
        session.close()