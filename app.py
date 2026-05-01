#import libraries
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from shared import listings, weekly_reviews

#UI
app_ui = ui.page_navbar(


    ui.nav_panel("Overview",

        ui.layout_sidebar(

            #sidebar
            ui.sidebar(
                ui.input_selectize(
                    "area_filter",
                    "Select Area",
                    choices=sorted(listings["neighbourhood"].unique().tolist()),
                    multiple=True
                ),

                ui.input_selectize(
                    "property_filter",
                    "Select Property Type",
                    choices=sorted(listings["room_type"].unique().tolist()),
                    multiple=True
                )
            ),

            #main (overview)
            ui.h3("Price Distribution"),
            ui.output_plot("price_hist"),

            ui.h3("Average Price by Neighbourhood"),
            ui.output_plot("price_bar"),
        )
    ),

    #top properties
    ui.nav_panel("Top Properties",

        ui.h3("Top 50 Listings by Reviews"),
        output_widget("top_bar"),

        ui.h3("Value Score (Reviews per Price)"),
        output_widget("value_scatter"),
    ),

    #map
    ui.nav_panel("Map",
        ui.h3("Top 50 Listings Map"),
        output_widget("map_plot")
    ),

    #reviews
    ui.nav_panel("Reviews",

        ui.h3("Reviews Over Time"),
        ui.output_plot("reviews_line"),

        ui.h3("Price vs Reviews"),
        output_widget("scatter_plot"),
    ),

    #insights
    ui.nav_panel("Insights",
        ui.h3("Correlation Heatmap"),
        ui.output_plot("heatmap")
    ),

    #title="Top 50 Dublin Airbnb Listings"
)

#server

def server(input, output, session):

    #reactive filter
    @reactive.calc
    def filtered_data():
        df = listings.copy()

        if input.area_filter():
            df = df[df["neighbourhood"].isin(input.area_filter())]

        if input.property_filter():
            df = df[df["room_type"].isin(input.property_filter())]

        return df

    #histogram
    @output
    @render.plot
    def price_hist():
        df = filtered_data()

        fig, ax = plt.subplots()
        sns.histplot(df["price"], bins=30, ax=ax)

        #ax.set_title("Price Distribution")
        ax.set_xlabel("Price")
        ax.set_ylabel("Count")

        return fig

    #avg price bar chart
    @output
    @render.plot
    def price_bar():
        df = filtered_data()

        avg_price = df.groupby("neighbourhood")["price"].mean().sort_values()

        fig, ax = plt.subplots()
        avg_price.plot(kind="bar", ax=ax)

        #ax.set_title("Average Price by Neighbourhood")
        ax.set_xlabel("Neighbourhood")
        ax.set_ylabel("Average Price")
        ax.tick_params(axis='x', rotation=45)

        return fig

    #top listings bar chart
    @output
    @render_widget
    def top_bar():
        fig = px.bar(
            filtered_data(),
            x="neighbourhood",
            y="number_of_reviews",
            color="room_type",
            #title="Top Listings by Reviews"
        )
        return fig

    #value score scatter plot
    @output
    @render_widget
    def value_scatter():
        fig = px.scatter(
            filtered_data(),
            x="price",
            y="value_score",
            color="room_type",
            hover_data=["neighbourhood"],
            #title="Value Score (Reviews per Price)"
        )
        return fig

    #plotly map
    @output
    @render_widget
    def map_plot():
        fig = px.scatter_map(
            filtered_data(),
            lat="latitude",
            lon="longitude",
            color="price",
            hover_data=["neighbourhood", "room_type", "price"],
            zoom=10,
            center={"lat": 53.35, "lon": -6.26}
        )
        return fig

    #time series
    @output
    @render.plot
    def reviews_line():
        fig, ax = plt.subplots()

        ax.plot(
            weekly_reviews["date"],
            weekly_reviews["review_count"]
        )

        ax.set_title("Weekly Reviews (4-week rolling average)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Reviews")

        return fig

    #scatter price vs reviews
    @output
    @render_widget
    def scatter_plot():
        fig = px.scatter(
            filtered_data(),
            x="price",
            y="number_of_reviews",
            color="room_type",
            hover_data=["neighbourhood"],
            #title="Price vs Reviews"
        )
        return fig

    #heatmap
    @output
    @render.plot
    def heatmap():
        df = filtered_data()

        corr = df[[
            "price",
            "number_of_reviews",
            #"neighbourhood",
            #"room_type",
            "minimum_nights"
        ]].corr()

        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

        #ax.set_title("Correlation Heatmap")
        return fig


#run app

app = App(app_ui, server)

#prevent server issue

if __name__ == "__main__":
    app.run(port=8001)