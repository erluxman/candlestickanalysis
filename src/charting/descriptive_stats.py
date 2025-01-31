def show_chart():
    # Load your data (replace this with your actual data loading)
    path_of_file = "/Users/laxmanbhattarai/projects/personal/mba/thesis_v2/data/step4_descriptive_stats/np/descriptive_stats.json"
    with open(path_of_file) as f:
        data = json.load(f)
    # Process data and create visualizations
    df = process_data(data)
    create_pvalue_plot(df, 0.05, "candlestick_pvalue_plot_0_05.html")
    create_pvalue_plot(df, 0.02, "candlestick_pvalue_plot_0_02.html")
    create_pvalue_plot(df, 0.01, "candlestick_pvalue_plot_0_01.html")
