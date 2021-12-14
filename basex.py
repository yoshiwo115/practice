from BaseXClient import BaseXClient
import re

# セッション作成
session = BaseXClient.Session('test-host', 1984, 'admin', 'admin')
foo = '綺麗だ/きれいだ'
bar = 'ガ格'

component_array = []

try:
    # DBオープン
    session.execute("open case")
    print(session.info())

    # DBの内容を表示 & 形式整え
    a = session.execute(f"xquery //entry[@headword='{foo}']/caseframe/argument[contains(@case,'{bar}')]/component")
    aa = a.replace('</component>', '')
    aaa = re.sub(r"[a-z]", '', aa)
    aaaa = re.sub(r"[0-9]", '', aaa)
    aaaaa = aaaa.replace("< =\"\">", '')
    # print(aaaaa)

    component_array = aaaaa.split("\n")
    print("正常終了しました\n")


finally:
    # セッションを閉じる
    if session:
        session.close()
    
    