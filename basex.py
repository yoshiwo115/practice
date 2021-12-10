from pathlib import Path
import os
import pprint
from BaseXClient import BaseXClient

# セッション作成
session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

try:
    # DBに格納するxmlファイル
    # xml_directory = Path("C:\Users\y-inoue\Desktop\kyoto-univ-web-cf-2.0") / "xml_data"
    # list_xml_path = sorted(xml_directory.glob("*.xml"), key=os.path.getmtime)
    # print("ロードするXMLファイル：")
    # pprint.pprint(list_xml_path)

    # DBオープン
    session.execute("open case")
    print(session.info())

    # xmlファイルを読み込んでDBに追加する
    # for path in list_xml_path:
    #     with open(path, mode='r', encoding="utf-8") as fi:
    #         str_xml = fi.read()

    #     session.add(path.name, str_xml)
    #     print(session.info())

    # DBの内容を表示
    print("\n" + session.execute("xquery //entry[@headword='綺麗だ/きれいだ']/caseframe/argument[contains(@case,'ガ格')]/component"))
    print("正常終了しました\n")

finally:
    # セッションを閉じる
    if session:
        session.close()