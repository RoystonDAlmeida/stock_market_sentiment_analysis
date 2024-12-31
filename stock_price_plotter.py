import streamlit as st
import plotly.graph_objects as go

def plot_stock_price_and_predictions(combined_data):
    """
    Plots the stock price over time and highlights the predicted movements interactively in Streamlit.

    @Args:
    - combined_data: DataFrame containing 'Date', 'Close', and 'target' columns.

    @Returns:
    - None: Displays the interactive plot in Streamlit.
    """

    # Create a figure
    fig = go.Figure()

    # Add stock price line
    fig.add_trace(go.Scatter(
        x=combined_data['Date'],
        y=combined_data['Close'],
        mode='lines',
        name='Stock Price',
        line=dict(color='blue'),
        hoverinfo='text',
        hovertext=combined_data['Close'].apply(lambda x: f'Price: ${x:.2f}')
    ))

    # Add scatter plot for predicted movements
    fig.add_trace(go.Scatter(
        x=combined_data['Date'],
        y=combined_data['Close'],
        mode='markers',
        name='Predicted Movement',
        marker=dict(color=combined_data['target'], colorscale='Viridis', size=8),
        hoverinfo='text',
        hovertext=combined_data.apply(
            lambda row: f'Date: {row["Date"]}<br>Price: ${row["Close"]:.2f}<br>Target: {row["target"]:.2f}', axis=1)
    ))

    # Update layout for better aesthetics
    fig.update_layout(
        title='Stock Price and Predicted Movements',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
        template='plotly_white'
    )

    # Display the interactive plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)