"""
在庫照合ツール用のサンプルCSVファイル作成スクリプト

生成されるファイル:
- data/honbu_list.csv （本部在庫リスト）
- data/tenpo_list.csv （店舗在庫リスト）
"""

import pandas as pd
import os

def create_sample_csv():
    # 設定
    data_dir = 'data'
    file_honbu = os.path.join(data_dir, 'honbu_list.csv')
    file_tenpo = os.path.join(data_dir, 'tenpo_list.csv')
    
    try:
        # 保存先のフォルダがなければ作成する
        os.makedirs(data_dir, exist_ok=True)

        # 1. 本部の在庫リスト（マスター）
        data_honbu = {
            '商品ID': ['A001', 'A002', 'A003', 'A004'],
            '商品名': ['りんご', 'バナナ', 'メロン', 'イチゴ'],
            '本部在庫': [100, 200, 50, 80]
        }

        # 2. 店舗から届いた実数リスト
        data_tenpo = {
            '商品ID': ['A001', 'A002', 'A003', 'A005'], # A004がなく、A005（未知）がある
            '商品名': ['りんご', 'バナナ', 'メロン', 'スイカ'],
            '店舗在庫': [100, 190, 50, 30] # バナナの数が本部と違う
        }

        # CSVファイルとして保存
        # encoding='utf-8-sig'
        pd.DataFrame(data_honbu).to_csv(file_honbu, index=False, encoding='utf-8-sig')
        pd.DataFrame(data_tenpo).to_csv(file_tenpo, index=False, encoding='utf-8-sig')

        print("✓ サンプルデータを作成しました。")
        print(f"  - {file_honbu}")
        print(f"  - {file_tenpo}")

    except PermissionError:  # ← こっちの方が発生しやすい
        print("❌ エラー：ファイルの書き込み権限がありません")
        print(f"   フォルダ: {data_dir}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    create_sample_csv()