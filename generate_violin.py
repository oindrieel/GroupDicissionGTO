import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Academic Journal Styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'grid.alpha': 0.4,
    'font.family': 'serif',
})


def generate_violin_plot():
    print("📊 Generating Violin Plot...")

    # 1. Load the benchmark data
    csv_path = "outputs/logs/real_benchmark_iterations.csv"
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{csv_path}'. Please run your benchmark script first.")
        return

    # 2. Select the columns to plot and rename them for the chart
    # (Adjust these keys if your CSV columns are named slightly differently)
    cols_to_plot = ['Smart_GTO', 'Static_GTO', 'PSO', 'GWO']

    available_cols = [c for c in cols_to_plot if c in df.columns]
    plot_df = df[available_cols].rename(columns={
        'Smart_GTO': 'Smart GTO\n(AI-Driven)',
        'Static_GTO': 'Static GTO\n(Baseline)',
        'PSO': 'PSO',
        'GWO': 'GWO'
    })

    # 3. Restructure data for seaborn (Melt)
    melted_df = plot_df.melt(var_name='Algorithm', value_name='Convergence Iterations')

    # 4. Draw the Plot
    plt.figure(figsize=(8, 5))

    # Use a custom color palette
    custom_palette = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e']

    sns.violinplot(
        x='Algorithm',
        y='Convergence Iterations',
        data=melted_df,
        hue='Algorithm',
        palette=custom_palette,
        inner='box',  # Shows the median and IQR inside the violin
        linewidth=1.5,
        alpha=0.8,
        legend=False
    )

    plt.title('Distribution of Convergence Iterations (30 Runs)')
    plt.ylabel('Iterations to Consensus (GCD > 0.95)')
    plt.xlabel('')

    # 5. Save it
    os.makedirs("outputs/plots", exist_ok=True)
    save_path = "outputs/plots/violin_plot_distribution.png"
    plt.tight_layout()
    plt.savefig(save_path, format='png', dpi=300)  # 300 DPI for journal quality
    plt.close()

    print(f"✅ Violin plot successfully generated at: {save_path}")


if __name__ == "__main__":
    generate_violin_plot()