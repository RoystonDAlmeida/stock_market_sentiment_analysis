import streamlit as st
import base64
from stock_price_data import get_stock_data_and_rows, get_company_name
from fetch_sentiment_data import fetch_sentiment_data
from preprocess_text import write_cleaned_contents_to_file
from perform_sentiment_analysis import get_sentiments_list
from combine_sentiment_and_stock_data import get_combined_sentiment_and_stock_data
from train_machine_learning_model import get_model_accuracy

# Set the page configuration
st.set_page_config(page_title="Stock Market Prediction using Sentiment Analysis", layout="wide")

# Title of the app
st.title("Stock Market Prediction using Sentiment Analysis")

# Create an interactive search bar
search_term = st.text_input("Search for a particular stock market (using ticker)", "")

if search_term:
    try:
        # Attempt to get the company name (using ticker)
        company_name = get_company_name(search_term)

        # Attempt to get stock data
        results_dataframe, results_dataframe_head, total_rows_size = get_stock_data_and_rows(search_term)

        # Display the DataFrame if it is not empty
        if not results_dataframe.empty:
            st.write(f"**{company_name}**")
            st.write("Head portion of the Dataframe")
            st.dataframe(results_dataframe)

            # Display additional information below the DataFrame
            dimensions = results_dataframe.shape
            st.write(f"**Dimensions:** {total_rows_size} rows x {dimensions[1]} columns")

            try:
                # Call the function fetch_sentiment_data with the search_term (ticker name)
                sentiment_description_list = fetch_sentiment_data(search_term)

                if len(sentiment_description_list) > 0:
                    # If sentiments are successfully fetched, print them (or display them in Streamlit)
                    st.write("**Sentiment Descriptions**:")

                    # Create columns for horizontal layout
                    cols = st.columns(4)

                    for i in range(min(3, len(sentiment_description_list))):  # Ensure we don't exceed available sentiments
                        with cols[i % 3]:  # Cycle through columns
                            sentiment = sentiment_description_list[i]
                            # Display date and title in a box
                            st.markdown(f"<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>"
                                        f"<strong>{sentiment['date']}</strong><br>"
                                        f"{sentiment['title']}</div>", unsafe_allow_html=True)

                    # Calculate the number of remaining sentiments
                    remaining_count = len(sentiment_description_list) - 3
                    if remaining_count > 0:
                        # Create a new column for the remaining count message
                        with cols[3]:  # Place it in the fourth column
                            st.markdown(
                                f"<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; text-align: center;'>"
                                f"<span style='color: gray;'>And {remaining_count} more</span></div>",
                                unsafe_allow_html=True)

                        try:
                            # Perform data preprocessing on the sentiment_description_list
                            write_cleaned_contents_to_file(sentiment_description_list)

                            # Display the title and create a download button for the text file
                            st.title("Formatted Sentiment Content Results")

                            # Load CSS styles for download button with icon
                            st.markdown("""
                            <style>
                            .download-button {
                                display: inline-flex;
                                align-items: center;
                                background-color: transparent; /* Make background transparent */
                                color: white; /* Text color */
                                padding: 10px 20px;
                                border: 2px solid white; /* White border */
                                border-radius: 5px;
                                cursor: pointer;
                                text-decoration: none;
                                font-size: 16px; /* Adjust font size */
                            }
                            .download-icon {
                                margin-right: 8px;
                            }
                            </style>
                            """, unsafe_allow_html=True)

                            # Create a download button for the cleaned sentiments file with proper base64 encoding
                            with open('cleaned_contents.csv', 'rb') as f:
                                file_content = f.read()
                                b64_content = base64.b64encode(file_content).decode()  # Encode to base64

                            href = f'''
                            <a class="download-button" href="data:text/plain;base64,{b64_content}" download="cleaned_contents.csv">
                                <i class="fas fa-download download-icon"></i>Download Formatted Sentiment Content
                            </a>
                            '''

                            st.markdown(href, unsafe_allow_html=True)

                            # Get the sentiment for each description in sentiments_description_list
                            sentiments_list = get_sentiments_list(sentiment_description_list)
                            # print(sentiments_list)[Contains {'compound','neg', 'neu', 'pos'}]

                            # Combine sentiments_list and stock_data
                            combined_data = get_combined_sentiment_and_stock_data(sentiment_description_list, sentiments_list, results_dataframe)

                            if not combined_data.empty:
                                # If combined_data dataframe is obtained
                                try:
                                    # Get the model metrics using combined_data
                                    cv_scores, mae, r2 = get_model_accuracy(combined_data)

                                    # Print the metrics
                                    st.write(f"**Model Evaluation metrics:**")
                                    st.write(f"**Cross-validated R-squared**: {cv_scores.mean():.2f}")
                                    st.write(f"**Mean Absolute Error**: {mae:.2f}")
                                    st.write(f"**R-squared**: {r2:.2f}")

                                except Exception as e:
                                    st.error(f"An error occurred while training the model: {str(e)}")

                        except Exception as e:
                            st.error(f"An error occurred while processing sentiment data: {str(e)}")
                else:
                    st.warning(f"No sentiment data available for {search_term}.")

            except Exception as e:
                # Handle any exceptions that occur during fetching
                st.error(f"An error occurred while fetching financial sentiment data for {search_term}: {str(e)}")

        else:
            st.warning("No data available for the given search term.")

    except ValueError as ve:
        # Display a specific error message if the company name is not found
        st.warning(str(ve))

    except Exception as e:
        # Display a general error message for other exceptions
        st.error(f"An error occurred: {e}")

# Include Font Awesome for icons (optional)
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True)
