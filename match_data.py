import pandas as pd
import os

def match_inventory():
    # 設定
    input_honbu = 'data/honbu_list.csv'
    input_tenpo = 'data/tenpo_list.csv'
    output_file = 'output/照合結果.xlsx'

    try:
        # 保存先ディレクトリの準備（安全策）
        dir_name = os.path.dirname(output_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # データ読み込み
        df_honbu = pd.read_csv(input_honbu, encoding='utf-8-sig')
        df_tenpo = pd.read_csv(input_tenpo, encoding='utf-8-sig')

        print(f"✓ 本部リスト読み込み: {len(df_honbu)}件")
        print(f"✓ 店舗リスト読み込み: {len(df_tenpo)}件")

        # 必須列の確認
        required_cols_honbu = ['商品ID', '商品名', '本部在庫']
        required_cols_tenpo = ['商品ID', '商品名', '店舗在庫']

        missing_honbu = [col for col in required_cols_honbu if col not in df_honbu.columns]
        missing_tenpo = [col for col in required_cols_tenpo if col not in df_tenpo.columns]

        if missing_honbu:
            print(f"❌ エラー：本部リストに必要な列がありません: {missing_honbu}")
            print(f"   現在の列: {df_honbu.columns.tolist()}")
            return

        if missing_tenpo:
            print(f"❌ エラー：店舗リストに必要な列がありません: {missing_tenpo}")
            print(f"   現在の列: {df_tenpo.columns.tolist()}")
            return

        # 2つのファイルを外部結合する
        df_merge = pd.merge(df_honbu, df_tenpo, on=['商品ID', '商品名'], how='outer', indicator=True)

        # 3. 状態（_merge列）の名前を分かりやすく書き換える
        df_merge['_merge'] = df_merge['_merge'].replace({
            'left_only': '本部のみに存在',
            'right_only': '店舗のみに存在',
            'both': '両方に存在'
        })

        # 4. 両方に存在し、かつ在庫数が数値で、かつ不一致の場合のみTrue
        df_merge['不一致'] = (
            (df_merge['_merge'] == '両方に存在') &
            (df_merge['本部在庫'].notna()) &
            (df_merge['店舗在庫'].notna()) &
            (df_merge['本部在庫'] != df_merge['店舗在庫'])
        )

        # 5. 結果をExcelで保存する
        df_merge.to_excel(output_file, index=False)

        print("照合が完了しました。『照合結果.xlsx』を確認してください。")
        print(f"\n【照合結果サマリー】")
        print(f"  - 照合総数: {len(df_merge)}件")
        print(f"  - 本部のみに存在: {(df_merge['_merge'] == '本部のみに存在').sum()}件")
        print(f"  - 店舗のみに存在: {(df_merge['_merge'] == '店舗のみに存在').sum()}件")
        print(f"  - 両方に存在: {(df_merge['_merge'] == '両方に存在').sum()}件")
        print(f"  - 在庫数不一致: {df_merge['不一致'].sum()}件")

    except FileNotFoundError:
        print("❌ エラー：dataフォルダの中に、必要なCSVファイルが見つかりません。")
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    match_inventory()