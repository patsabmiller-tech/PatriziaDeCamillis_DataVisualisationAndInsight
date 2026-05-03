#import libraries
from pathlib import Path
import pandas as pd

#app directory
app_dir = Path(__file__).parent

#load data
listings = pd.read_csv(app_dir / "listings.csv")
weekly_reviews = pd.read_csv(app_dir / "weekly_reviews.csv")

#ensure datetime
#visualisation doesn't show properly if this is not repeated
weekly_reviews["date"] = pd.to_datetime(weekly_reviews["date"])

