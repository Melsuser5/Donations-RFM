import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
pd.options.display.float_format = '{:.2f}'.format

df = pd.read_csv('https://raw.githubusercontent.com/Melsuser5/Donations-RFM/main/donations_rfm_final.csv')
custom_palette = ["#5a8eb8", "#5ab874", "#bf3636", "#f08922", "#8146d4", "#e3528e", "#2a9ac7"]

df["Segment"] = df["overall_score"].astype(str)
fig_all = px.scatter_3d(df, x='recency', y='frequency', z='revenue', color='Segment',width=1600, height=800)
log_fig = px.scatter_3d(df, x='recency', y='frequency', z='revenue', color='Segment', log_x=False,log_y=True,log_z=True, width=1600, height=800,color_continuous_scale=custom_palette)


st.set_page_config(layout="centered")
st.set_option('deprecation.showPyplotGlobalUse', True)
st.title("Philanthropy RFM Segmentation Dashboard")
st.subheader("Customer Segmentation using RFM Analysis")
st.markdown(''' RFM (Recency, Frequency, Monetary Value) Analysis is a data driven customer segmentation technique that assigns a score to customers  based on the combination of three variables:
- Their last purchase,  
- How often they have purchased in the past, and  
- How much they have spent overall.  

This model can be used to identify distinct customer segments and target them more directly.  
We can gain insights into the preferences and needs of different groups. This will enable us to tailor our marketing efforts to them.''')



option = st.selectbox("Use the dropdown to see how dense each segment is", ("Segments", "Show Density of Segments"))
if option == "Segments":
    st.plotly_chart(fig_all, use_container_width=True)
elif option == "Show Density of Segments":
    st.plotly_chart(log_fig, use_container_width=True)

st.header("Segment Descriptions and Database Count")

segment_data = [
    {"Segment":0,"Description": "Subs who have not donated in 1+ years","Customer Count":10251 },
    {"Segment":1, "Description": " Single tix buyers who have not donated in 1+ years", "Customer Count": 25359},
    {"Segment":2, "Description": "Single tix buyers", "Customer Count": 160},
    {"Segment":3, "Description": "Major Donors 10K +", "Customer Count": 41},
    {"Segment":4, "Description": "Sub who donate with subscription", "Customer Count": 264}

]
seg_count = pd.DataFrame(segment_data)
seg_count.set_index(['Segment'],inplace=True)

st.table(seg_count)

sub_counts = df.groupby(['overall_score']).size().reset_index(name='count')

# Plot the count plot
plt.figure(figsize=(10, 6))
sns.barplot(x='overall_score', y='count', hue ='count', data=sub_counts)
plt.xlabel('Segment')
plt.ylabel('Count')
plt.title('Number of Customers by Segment')
plt.yscale('log')
st.pyplot(plt)


st.header("Segments and Donation Channels")

segment_revenue = df.groupby(['overall_score', 'donation_source'])['revenue'].sum().reset_index()

# Create a bar plot with the y-axis representing revenue
plt.figure(figsize=(10, 6))
sns.barplot(x='overall_score', y='revenue', hue='donation_source', data=segment_revenue)
plt.xlabel('overall_score')
plt.ylabel('Revenue')
plt.title('Segments and Donation Channels')
plt.legend(title='Donation Source')
plt.gca().ticklabel_format(style='plain', axis='y')
st.pyplot(plt)

st.markdown(''' This plot shows the total amount donated by each segment, broken down by channel. The Web channel is by far the largest source of donations across all segements. 
Notable also is the ammount processed via the box office channel in segment 3.''')
st.subheading("Possible Next Actions")
st.markdown('''- Combining Mosaic data, campaign response data, ticket purchase data to create a customer profile
- Monitor growth of segments to track trends''')
