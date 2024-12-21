# 株式会社燈 2024-12-21 生成AIハッカソンの成果物。

### 使い方
- まず、事前にopenai api, tavity api, googlemap apiを取得し、.env_exampleを.envに書き換えて、キーをセットすること

1. プロジェクトのルートで`docker-compose up`を実行
2. `dokcer ps`でweb_containerのプロセスIDを取得、`docker exec -it <ID> /bin/bash`でコンテナ内に入る
3. /workspace/src/main.py を実行。