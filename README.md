# OS-Copilot：自己改善を伴う汎用コンピュータエージェントに向けて

<div align="center">

[[ウェブサイト]](https://os-copilot.github.io/)
[[Arxiv]](https://arxiv.org/abs/2402.07456)
[[PDF]](https://arxiv.org/pdf/2402.07456.pdf)
<!-- [[ツイート]](https://twitter.com/DrJimFan/status/1662115266933972993?s=20) -->

[![スタティックバッジ](https://img.shields.io/badge/MIT-License-green)](https://github.com/OS-Copilot/FRIDAY/blob/main/LICENSE)
![スタティックバッジ](https://img.shields.io/badge/python-3.10-blue)
[![スタティックバッジ](https://img.shields.io/badge/FRIDAY-Frontend-yellow)](https://github.com/OS-Copilot/FRIDAY-front)

<p align="center">
  <img src='pic/demo.png' width="100%">
</p>

</div>

## 概要

- **OS-Copilot**は、LinuxとMacOS上で汎用コンピュータエージェントを構築するための先駆的な概念フレームワークであり、異種OSエコシステム内でのアプリケーション間の統一インターフェースを提供します。

<p align="center">
  <img src='pic/framework.png' width="75%">
</p>

- OS-Copilotを活用して、一般的なコンピュータタスクを解決する能力を持つ自己改善型AIアシスタント**FRIDAY**を構築しました。

<p align="center">
  <img src='pic/FRIDAY.png' width="75%">
</p>

## ⚡️ クイックスタート

1. **GitHubリポジトリをクローンする:**

```

git clone [https://github.com/OS-Copilot/FRIDAY.git](https://github.com/OS-Copilot/FRIDAY.git) 

```


2. **Python環境を設定する:** バージョン3.10以上のPython環境があることを確認してください。以下のコマンドを使用して、この環境を作成・アクティベートできます（`FRIDAY_env`を好みの環境名に置き換えてください）:

```
conda create -n FRIDAY_env python=3.10 -y
conda activate FRIDAY_env

```

3. **依存関係をインストールする:** `FRIDAY`ディレクトリに移動し、必要な依存関係をインストールするために次のコマンドを実行します:

```
cd FRIDAY
pip install -r requirements.txt

```

4. **OpenAI APIキーを設定する:** [.env](.env)にあなたのOpenAI APIキーを設定し、使用したいモデルを選択してください。

5. **タスクを実行する:** 次のコマンドを実行してFRIDAYを起動します。必要に応じて`[query]`をあなたのタスクに置き換えてください。デフォルトのタスクは「'agent'という単語を含むテキストファイルを'document'というフォルダから'working_dir/agent'というパスに移動する」です。タスクが関連ファイルの使用を必要とする場合、`--query_file_path [file_path]`を使用できます。

```
python run.py --query [query]

```


* FRIDAYは現在、単一ラウンドの会話のみをサポートしています。

## FRIDAY-Gizmos
FRIDAY内で直接使用できるツールを含む、FRIDAYのためのオープンソースライブラリを維持しています。
ツールの詳細なリストについては、[FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos)をご覧ください。使用方法は以下の通りです:

1. [FRIDAY-Gizmos](https://github.com/OS-Copilot/FRIDAY-Gizmos)で使用したいツールを見つけ、そのツールコードをダウンロードします。
2. ツールをFRIDAYのツールキットに追加します:
```shell
python friday/core/action_manager.py --add --tool_name [tool_name] --tool_path [tool_path]
```


1. ツールを削除したい場合は、次のコマンドを実行できます:

```shell
python friday/core/action_manager.py --delete --tool_name [tool_name]
```


## ユーザーインターフェース (UI)

**直感的なフロントエンドで体験を向上させましょう！**  このインターフェースは、あなたのエージェントを容易に制御するために作られています。詳細については、[FRIDAY Frontend](https://github.com/OS-Copilot/FRIDAY-front) をご覧ください。
## FastAPIを使用して自分のAPIツールをデプロイする

すべてのFastAPIはこちらにあります： [friday/api](https://chat.openai.com/c/friday/api)  
1. **FastAPIファイルを準備する:**  [friday/api](https://chat.openai.com/c/friday/api) の下に新しいapiフォルダを作成し、そのフォルダの下にFastAPIのPythonファイルを配置します。 
2. **APIサーバーにFastAPIをインポートする:**  [friday/core/api_server.py]() であなたのapiをインポートします：

```python
import os

from fastapi import FastAPI
from friday.core.server_config import ConfigManager

app = FastAPI()


from friday.api.bing.bing_service as bing_router
#[TODO] ここに自分のapiをインポートしてください


from starlette.middleware.base as BaseHTTPMiddleware
from starlette.requests as Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"着信リクエスト: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            print(f"リクエストエラー: {str(e)}")
            raise e from None
        else:
            print(f"発信レスポンス: {response.status_code}")
        return response


app.add_middleware(LoggingMiddleware)

# サービス名とそのルーターをマッピングする辞書を作成します
services = {
    "bing": bing_router,
    # [TODO] ここにapiルーターを追加してください

}

server_list = [
    "bing",
    # [TODO] ここにapiのサービス名を追加してください。
]

# server_listに記載されているサービスのルーターのみを含めます
for service in server_list:
    if service in services:
        app.include_router(services[service])

# proxy_manager = ConfigManager()
# proxy_manager.apply_proxies()

if __name__ == "__main__":
    import uvicorn
    # ポートを変更することができます
    uvicorn.run(app, host="0.0.0.0", port=8079)
```

 
1. **APIサーバーを実行する:** 
サーバーをlocalhostで実行するか、またはあなたのウェブサーバーにデプロイします:

```Copy code
python api_server.py
```

 
1. **APIドキュメントを更新する:**

[friday/core/openapi.json](https://chat.openai.com/c/friday/core/openapi.json) にあるAPIドキュメントを更新してください。APIサーバーを起動した後、`http://localhost:8079/openapi.json`で現在のOpenAPIドキュメントにアクセスできます。

各APIの概要を徹底的に更新し、その機能と使用方法を明確に説明してください。これは、FRIDAYが各APIの目的を理解するために重要です。

例えば:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {  
    "/tools/audio2text": {
      "post": {
        // [TODO] あなたのapiの使用法を説明するために概要を変更してください。
        "summary": "音声を自然言語テキストに変換するツール",
        "operationId": "audio2text_tools_audio2text_post",
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "$ref": "#/components/schemas/Body_audio2text_tools_audio2text_post"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "成功したレスポンス",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "検証エラー",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    
  },
  "components": {
    "schemas": {
      "Body_audio2text_tools_audio2text_post": {
        "properties": {
          "file": {
            "type": "string",
            "format": "binary",
            "title": "ファイル"
          }
        },
        "type": "object",
        "required": [
          "file"
        ],
        "title": "Body_audio2text_tools_audio2text_post"
      },
      
      
    }
  }
}
```

 
1. **tool_request_util.pyのベースURLを変更する:**  FRIDAYは、[friday/core/tool_request_util.py](https://chat.openai.com/c/friday/core/tool_request_util.py) にあるスクリプトを使用してAPIツールとインターフェースします。APIをデプロイした後、このファイルのベースURLをあなたのAPIサーバーのURLに一致するように更新してください。

```python
import requests
class ToolRequestUtil:
    def __init__(self):
        self.session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        # [TODO] ベースURLを変更してください
        self.base_url = "http://localhost:8079"

    def request(self, api_path, method, params=None, files=None, content_type="application/json"):
        """
        :param api_path: apiのパス
        :param method: get/post
        :param params: apiのパラメータ、Noneも可
        :param files: アップロードするファイル、Noneも可
        :param content_type: apiのcontent_type、例：application/json, multipart/form-data、Noneも可
        :return: apiの返り値
        """
        url = self.base_url + api_path
        try:
            if method.lower() == "get":
                if content_type == "application/json":
                    result = self.session.get(url=url, json=params, headers=self.headers, timeout=60).json()
                else: 
                    result = self.session.get(url=url, params=params, headers=self.headers, timeout=60).json()
            elif method.lower() == "post":
                if content_type == "multipart/form-data":
                    result = self.session.post(url=url, files=files, data=params, headers=self.headers).json()
                elif content_type == "application/json":
                    result = self.session.post(url=url, json=params, headers=self.headers).json()
                else:
                    result = self.session.post(url=url, data=params, headers=self.headers).json()
            else:
                print("リクエストメソッドエラー！")
                return None
            return result
        except Exception as e:
            print("HTTPリクエストエラー: %s" % e)
            return None
```


## 免責事項

OS-Copilotは「現状のまま」提供され、いかなる種類の保証も伴いません。ユーザーは使用に伴うあらゆるリスク、**潜在的なデータ損失** や**システム設定の変更** を含む、全責任を負います。OS-Copilotの開発者は、その使用から生じるいかなる損害や損失に対しても責任を負いません。ユーザーは、行動が適用される法律および規制に準拠していることを確認する必要があります。
## 🏫 コミュニティ

エージェント愛好家とつながり、ツールやデモを共有し、エキサイティングなイニシアチブに協力するために、私たちのコミュニティに参加してください。[Slack](https://join.slack.com/t/slack-ped8294/shared_invite/zt-2cqebow90-soac9UFKGZ2RcUy8PqjZrA) で私たちを見つけることができます。

## 引用

```css
@misc{wu2024oscopilot,
      title={OS-Copilot: 自己改善を伴う汎用コンピュータエージェントに向けて}, 
      author={Zhiyong Wu and Chengcheng Han and Zichen Ding and Zhenmin Weng and Zhoumianze Liu and Shunyu Yao and Tao Yu and Lingpeng Kong},
      year={2024},
      eprint={2402.07456},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```


## 📬 連絡先

ご質問、提案、または何らかの理由で私たちに連絡したい場合は、[wuzhiyong@pjlab.org.cn]() までメールでお気軽にご連絡ください。