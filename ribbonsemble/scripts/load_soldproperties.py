import load_properties as lp 
import os
import sys
import subprocess
import datetime
import pickle
import pandas as pd
from django.core.wsgi import get_wsgi_application
import json
from dateutil import parser

def find_latest_soldpx_csvname(specific_date='<YYYYMMDD>'):
    """Finds the newest csv name in the drive.  Can pull a specific date
       by filling in the specific date field.

    Keyword arguments:
        specific date: [string in YYYYMMDD date format ] This is optional.  Standard it to leave blank and it will 
                        pull the latest.

    Returns:
        returns a csv filename to pull from google storage bucket.
    """
    command = ['gsutil','ls','gs://rooftop-data/sold_home_data/']
    out = subprocess.check_output(command)
    csv_list = str(out).split('\\n')
    parsed_csv_list = [x[x.find('data_')+5:-4] for x in csv_list]
    date_csv_list = [x for x in parsed_csv_list if len(x)==8]
    dates = [parser.parse(x) for x in date_csv_list]
    now = datetime.datetime.now()
    newest = max(dt for dt in dates if dt < now)
    csv_filename = 'soldhomedata_{}.csv'.format(newest.strftime('%Y%m%d'))
    return csv_filename

def url_string_to_json(url_string):
    """This take is string of urls and returns a JSON of image gallery paths
    
    Keyword arguments:
        url_string: [string] string of image gallery paths

    Returns:
        image_gallery_json: [JSON] a json of the image gallery paths
    """
    json_list = url_string.split(';')
    string_as_json = json.dumps(json_list)
    return string_as_json

def create_sold_property_object(df, idx):
    """Creates django property model object when given a dataframe of new 
       listing data and index number
    
    Keyword arguments:
        df: [pandas dataframe object] dataframe object of home listing data
        idx: index in the dataframe of the house we are turning into a property object

    Returns:
        home: [django model] property object generated from the data in the row
        of the listing dataframe 
    """   
    home, created = SoldProperty.objects.update_or_create(

            # Address
            street_address_1 = df.iloc[idx]['address_address_line1'],
            street_address_2 = df.iloc[idx]['address_unit'],
            city = df.iloc[idx]['address_city'],
            state = df.iloc[idx]['address_state'],
            zip_code = df.iloc[idx]['address_zipcode'],
            latitude = df.iloc[idx]['address_lat'],
            longitude = df.iloc[idx]['address_lon'],
            
            # Address keys
            hc_slug=df.iloc[idx]['Unnamed: 0'],
            lowercase_slug = df.iloc[idx]['Unnamed: 0'].lower(),
            
            # Listing data
            sold_price = df.iloc[idx]['listing_data_sale_price'],
            num_bedrooms = df.iloc[idx]['listing_data_num_bedrooms'],
            num_bathrooms = df.iloc[idx]['listing_data_num_bathrooms'],
            building_area_sq_ft = df.iloc[idx]['listing_data_building_area_sq_ft'],
            home_type = df.iloc[idx]['listing_data_home_type'],
            sale_price_history = pricehist2json(df.iloc[idx]['listing_data_sale_history']),

            # Features
            num_floors = df.iloc[idx]['features_floors'],
            year_built = df.iloc[idx]['features_year_built'],
            listing_status = df.iloc[idx]['features_listing_status'],
            interior_features = df.iloc[idx]['features_interior_features'],
            flooring = df.iloc[idx]['features_flooring'],
            is_foreclosure = df.iloc[idx]['features_is_foreclosure'],
            remax_url = df.iloc[idx]['features_remax_url'],
            rx_num_half_bath = df.iloc[idx]['features_num_half_bath'],
            has_septic = df.iloc[idx]['features_has_septic'],
            has_pool = df.iloc[idx]['features_has_pool'],
            subdivision = df.iloc[idx]['features_subdivision'],
            has_established_subdivision = df.iloc[idx]['features_has_established_subdivision'],
            has_well = df.iloc[idx]['features_has_well'],
            has_garage = df.iloc[idx]['features_has_garage'],
            no_pool_well_septic = df.iloc[idx]['features_no_pool_well_septic'],
            garage_size = df.iloc[idx]['features_garage_detail'],
            rx_num_full_bath = df.iloc[idx]['features_num_full_bath'],
            description = df.iloc[idx]['features_desc'],

            # Images
            img_path_header = '/img/'+df.iloc[idx]['Unnamed: 0']+'/img1.jpg',
            img_paths_gallery = url_string_to_json(';'.join(['/img/' + df.iloc[idx]['Unnamed: 0'] + '/img'
                                     + str(x) + '.jpg' for x, y in enumerate(df.iloc[idx]
                                     ['images_img_gallery'].split(';'))]))
        )
    return home, created

def iterate_through_soldhome_properties_and_create_models(df):
    """Iterates through homes in a dataframe, creates a property object, and saves to db
    
    Keyword arguments:
        df: [django dataframe object] this is the cleaned and filtered dataframe of
        the houses

    Returns:
        There is no output but this simply loops through the dataframe, creates a property
        object of each home which is represented by a row in the dataframe, and then
        attempts to save the created property object to the database.

        If a property object with the same slug already exists in the dataframe,
        this will fail.
    """
    print('Loading sold home properties to db:')
    save_count = 0
    fail_count = 0
    for idx in range(len(df)):
        try:
            property_object, created = create_sold_property_object(df, idx)
            save_count += created
        except Exception as e:
            fail_count += 1
            print('saving home failed, exception: {}'.format(e))
    print('saved: {} failed: {}  success_rate: {}%'.format(save_count,fail_count,
                                                            str(100*float(save_count/(save_count
                                                                      +fail_count)))))

def cleaned_soldhome_dataframe_from_csv(csv_file_path):
    """Takes a csv, turns it into a dataframe, and cleans with ribbon buy box

    Keyword arguments:
        csv_file_path: [string] location of the csv dataframe

    Returns:
        cleaned_and_filtered_df: [pandas dataframe object] dataframe object
    """
    csv_path = os.path.join(os.getcwd(), csv_file_path)
    df = pd.read_csv(csv_path)
    df = df.where((pd.notnull(df)), None)
    df = df.drop_duplicates(subset='Unnamed: 0')
    cleaned_and_filtered_df = df[
        (df['listing_data_num_bathrooms']>=1) 
        & (df['listing_data_num_bedrooms']>=1)
        & (df['listing_data_home_type']=='Single Family')
        & (df['listing_data_sale_price']>=50000)
        & (df['listing_data_sale_price']<=2000000)
        & (df['features_year_built']>=1900)
        ]
    return cleaned_and_filtered_df

def pricehist2json(salelist):
    d={}
    try:
        salelist = salelist.split(';')
    except:
        return json.dumps(None) 
    iseven = len(salelist) % 2 == 0
    if iseven:
        for idx,data in enumerate(salelist):
            if idx%2 == 0:
                datakey = data
                d[data] = 0
            if idx%2 == 1:
                d[datakey] = data
        return json.dumps(d)
    else:
        return json.dumps(None)

if __name__ == '__main__':
    # Check current location
    lp.check_currentdir_location()
    # Setup django environment.  Note must run from the rooftop
    lp.setup_environment()
    # Need to import Property here and not at top of script because need env setup first.
    from hedonic_model.models import SoldProperty
    # Get the name of the more recently updated csv file
    csv_filename = find_latest_soldpx_csvname()
    # Pull csv from google cloud storage
    lp.fetch_from_google_storage('rooftop-data','sold_home_data',csv_filename,
                              'scripts/csv_data')
    soldproperties_df = cleaned_soldhome_dataframe_from_csv('scripts/csv_data/{}'.format(csv_filename))
    iterate_through_soldhome_properties_and_create_models(soldproperties_df)