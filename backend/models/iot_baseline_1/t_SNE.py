import joblib  # For saving and loading t-SNE results
import os
import json  # To format the output as JSON

# File paths for saving/loading t-SNE results
tsne_data_file = 'tsne_results.pkl'
tsne_image_file = 'tsne_plot.png'

# Function to load saved t-SNE results without recalculating
def load_tsne_results():
    if os.path.exists(tsne_data_file) and os.path.exists(tsne_image_file):
        print("Loading existing t-SNE results...")
        with open(tsne_data_file, 'rb') as f:
            tsne_data = joblib.load(f)
            return tsne_data['tsne_plot_image'], tsne_data['tsne_coordinates'], tsne_data['selected_clusters']
    else:
        raise FileNotFoundError("t-SNE results not found. You need to run the t-SNE calculation first.")

# Try to load t-SNE results and print them in JSON format
try:
    tsne_plot_image, tsne_coordinates, selected_clusters = load_tsne_results()
    print(f"t-SNE results loaded successfully from '{tsne_data_file}'.")

    # 构建 JSON 数据
    tsne_data_json = {
        "tsne_plot_image": tsne_plot_image,
        "selected_clusters": selected_clusters,
        "tsne_coordinates": tsne_coordinates
    }

    # 以 JSON 格式打印 t-SNE 结果
    print("\nt-SNE Results in JSON format:\n")
    print(json.dumps(tsne_data_json, indent=4, ensure_ascii=False))

except FileNotFoundError as e:
    print(e)
