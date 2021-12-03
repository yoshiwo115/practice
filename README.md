# practice

練習用環境  

Dockerfile更新してイメージを更新するとき  
docker build -t yoshiwo115/practiceenv:latest .
docker-compose up --build  

・コンテナ稼働状況確認
docker ps -a

・コンテナ内に入るとき  
docker exec -it containerID /bin/bash  
dockerのCLIでコマンド操作、ファイル実行  
  
・powershellでのheadとtail  
Get-Content "kyoto-univ-web-cf-2.0.xml"-Encoding UTF8 | Select-Object -first 100  
Get-Content "kyoto-univ-web-cf-2.0.xml"-Encoding UTF8 | Select-Object -last 100 

・powershell:特定の文字列の後の何行かを取る 
Select-String -Path "kyoto-univ-web-cf-2.0.xml" -Encoding UTF8 -Pattern "<entry headword=`"綺麗だ/きれいだ`"" -Context 0, 1 

・grep的なpowershellコマンド
Select-String "美味しい/おいしい" kyoto-univ-web-cf-2.0.xml -Encoding UTF8  

・baseXの検索例 
//entry[@headword="綺麗だ/きれいだ"]/caseframe/argument[contains(@case,"ガ格")]/component