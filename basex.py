from BaseXClient import BaseXClient

# セッション作成
session = BaseXClient.Session('test-host', 1984, 'admin', 'admin')
foo = '綺麗だ/きれいだ'
bar = 'ガ格'
a = ''

component_array = []

try:
    # DBオープン
    session.execute("open case")
    print(session.info())

    # DBの内容を表示
    a =  "\n" + session.execute(f"xquery //entry[@headword='{foo}']/caseframe/argument[contains(@case,'{bar}')]/component")
    print(a)
    component_array.append(a)
    print("正常終了しました\n")
    
    print(component_array[0])
    print('component_array')


finally:
    # セッションを閉じる
    if session:
        session.close()