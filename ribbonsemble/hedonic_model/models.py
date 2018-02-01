"""Common model definitions.
"""
import jsonfield
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.postgres import fields as postgres_fields
from django.db import models
from django.utils import timezone
from model_utils import FieldTracker


# Only use 3rd party JSONField for SQLite.
JSONField = (jsonfield.JSONField if settings.USING_SQLITE_DB else
             postgres_fields.JSONField)


class SoldProperty(models.Model):
    """A property that may or may not be on the market for sale.
    Not tied to specific users.
    """
    # ============= Address =============
    street_address_1 = models.CharField(max_length=191)
    street_address_2 = models.CharField(max_length=191, blank=True, null=True)
    city = models.CharField(max_length=191)
    state = models.CharField(max_length=191)
    zip_code = models.CharField(max_length=15)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    # ============= Address keys =============
    # House Canary slug is capitalized e.g. '16-Meadow-Ln-Pelham-NH-41239'
    hc_slug = models.SlugField(max_length=191, unique=True) # Has db_index by default.
    # Internal lowercase slug e.g. '16-meadow-ln-pelham-nh-41239'
    lowercase_slug = models.SlugField(max_length=191) # Has db_index by default.

    # ============= Listing data =============
    sold_price = models.BigIntegerField(blank=True, null=True)
    num_bedrooms = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True)
    num_bathrooms = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True)
    building_area_sq_ft = models.PositiveIntegerField(blank=True, null=True)
    home_type = models.CharField(max_length=280,blank=True,null=True)
    sale_price_history = models.TextField(blank=True,null=True)

    # ============= Valuation =============
    # Ribbon guaranteed max bid for property, assuming enough Buying Power.
    certified_max_bid = models.BigIntegerField(null=True, blank=True)
    certified_max_bid_created_at = models.DateTimeField(null=True, blank=True)

    house_canary_avm = models.BigIntegerField(null=True, blank=True)
    red_bell_ave = models.BigIntegerField(null=True, blank=True)
    red_bell_ar_bpo = models.BigIntegerField(null=True, blank=True)
    red_bell_bpo = models.BigIntegerField(blank=True, null=True)
    
    # ============= Features =============
    
    num_floors = models.PositiveIntegerField(blank=True, null=True)
    rx_num_half_bath = models.PositiveIntegerField(blank=True, null=True)
    rx_num_full_bath = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    listing_status = models.CharField(max_length=280, blank=True, null=True)
    flooring = models.CharField(max_length=280, blank=True, null=True)
    interior_features = models.CharField(max_length=280, blank=True, null=True)
    remax_url = models.CharField(max_length=500, blank=True, null=True)
    subdivision = models.CharField(max_length=280, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_foreclosure = models.NullBooleanField(blank=True, null=True)
    has_septic = models.NullBooleanField(blank=True, null=True)
    has_pool = models.NullBooleanField(blank=True, null=True)
    has_established_subdivision = models.NullBooleanField(blank=True, null=True)
    has_well = models.NullBooleanField(blank=True, null=True)
    has_garage = models.NullBooleanField(blank=True, null=True)
    no_pool_well_septic = models.NullBooleanField(blank=True, null=True)
    local_school_quality = models.PositiveIntegerField(blank=True, null=True)
    rx_date_listed = models.CharField(max_length=280, blank=True, null=True)
    garage_size = models.PositiveIntegerField(blank=True, null=True) 
    mls_listing_id = models.BigIntegerField(blank=True, null=True)
    
    # =========== ImageInfo ===========
    
    img_path_header = models.CharField(max_length=280, blank=True, null=True)
    img_paths_gallery = JSONField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return '%s, %s, %s, %s %s. Max bid %s' % (
            self.street_address_1,
            self.street_address_2,
            self.city,
            self.state,
            self.zip_code,
            self.certified_max_bid,
        )	

class ListProperty(models.Model):
    """A property that may or may not be on the market for sale.
    Not tied to specific users.
    """
    # ============= Address =============
    street_address_1 = models.CharField(max_length=191)
    street_address_2 = models.CharField(max_length=191, blank=True, null=True)
    city = models.CharField(max_length=191)
    state = models.CharField(max_length=191)
    zip_code = models.CharField(max_length=15)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    # ============= Address keys =============
    # House Canary slug is capitalized e.g. '16-Meadow-Ln-Pelham-NH-41239'
    hc_slug = models.SlugField(max_length=191, unique=True) # Has db_index by default.
    # Internal lowercase slug e.g. '16-meadow-ln-pelham-nh-41239'
    lowercase_slug = models.SlugField(max_length=191) # Has db_index by default.

    # ============= Listing data =============
    list_price = models.BigIntegerField(blank=True, null=True)
    num_bedrooms = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True)
    num_bathrooms = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True)
    building_area_sq_ft = models.PositiveIntegerField(blank=True, null=True)
    home_type = models.CharField(max_length=280,blank=True,null=True)
    
    # ============= Valuation =============
    # Ribbon guaranteed max bid for property, assuming enough Buying Power.
    certified_max_bid = models.BigIntegerField(null=True, blank=True)
    certified_max_bid_created_at = models.DateTimeField(null=True, blank=True)

    house_canary_avm = models.BigIntegerField(null=True, blank=True)
    red_bell_ave = models.BigIntegerField(null=True, blank=True)
    red_bell_ar_bpo = models.BigIntegerField(null=True, blank=True)
    red_bell_bpo = models.BigIntegerField(blank=True, null=True)
    
    # ============= Features =============
    
    num_floors = models.PositiveIntegerField(blank=True, null=True)
    rx_num_half_bath = models.PositiveIntegerField(blank=True, null=True)
    rx_num_full_bath = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    listing_status = models.CharField(max_length=280, blank=True, null=True)
    flooring = models.CharField(max_length=280, blank=True, null=True)
    interior_features = models.CharField(max_length=280, blank=True, null=True)
    remax_url = models.CharField(max_length=500, blank=True, null=True)
    subdivision = models.CharField(max_length=280, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_foreclosure = models.NullBooleanField(blank=True, null=True)
    has_septic = models.NullBooleanField(blank=True, null=True)
    has_pool = models.NullBooleanField(blank=True, null=True)
    has_established_subdivision = models.NullBooleanField(blank=True, null=True)
    has_well = models.NullBooleanField(blank=True, null=True)
    has_garage = models.NullBooleanField(blank=True, null=True)
    no_pool_well_septic = models.NullBooleanField(blank=True, null=True)
    local_school_quality = models.PositiveIntegerField(blank=True, null=True)
    rx_date_listed = models.CharField(max_length=280, blank=True, null=True)
    garage_size = models.PositiveIntegerField(blank=True, null=True) 
    mls_listing_id = models.BigIntegerField(blank=True, null=True)
    
    # =========== ImageInfo ===========
    
    img_path_header = models.CharField(max_length=280, blank=True, null=True)
    img_paths_gallery = JSONField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return '%s, %s, %s, %s %s. Max bid %s' % (
            self.street_address_1,
            self.street_address_2,
            self.city,
            self.state,
            self.zip_code,
            self.certified_max_bid,
        )
