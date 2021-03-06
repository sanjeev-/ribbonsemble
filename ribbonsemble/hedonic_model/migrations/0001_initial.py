# Generated by Django 2.0 on 2018-02-01 20:24

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address_1', models.CharField(max_length=191)),
                ('street_address_2', models.CharField(blank=True, max_length=191, null=True)),
                ('city', models.CharField(max_length=191)),
                ('state', models.CharField(max_length=191)),
                ('zip_code', models.CharField(max_length=15)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('hc_slug', models.SlugField(max_length=191, unique=True)),
                ('lowercase_slug', models.SlugField(max_length=191)),
                ('list_price', models.BigIntegerField(blank=True, null=True)),
                ('num_bedrooms', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('num_bathrooms', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('building_area_sq_ft', models.PositiveIntegerField(blank=True, null=True)),
                ('home_type', models.CharField(blank=True, max_length=280, null=True)),
                ('certified_max_bid', models.BigIntegerField(blank=True, null=True)),
                ('certified_max_bid_created_at', models.DateTimeField(blank=True, null=True)),
                ('house_canary_avm', models.BigIntegerField(blank=True, null=True)),
                ('red_bell_ave', models.BigIntegerField(blank=True, null=True)),
                ('red_bell_ar_bpo', models.BigIntegerField(blank=True, null=True)),
                ('red_bell_bpo', models.BigIntegerField(blank=True, null=True)),
                ('num_floors', models.PositiveIntegerField(blank=True, null=True)),
                ('rx_num_half_bath', models.PositiveIntegerField(blank=True, null=True)),
                ('rx_num_full_bath', models.PositiveIntegerField(blank=True, null=True)),
                ('year_built', models.PositiveIntegerField(blank=True, null=True)),
                ('listing_status', models.CharField(blank=True, max_length=280, null=True)),
                ('flooring', models.CharField(blank=True, max_length=280, null=True)),
                ('interior_features', models.CharField(blank=True, max_length=280, null=True)),
                ('remax_url', models.CharField(blank=True, max_length=500, null=True)),
                ('subdivision', models.CharField(blank=True, max_length=280, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_foreclosure', models.NullBooleanField()),
                ('has_septic', models.NullBooleanField()),
                ('has_pool', models.NullBooleanField()),
                ('has_established_subdivision', models.NullBooleanField()),
                ('has_well', models.NullBooleanField()),
                ('has_garage', models.NullBooleanField()),
                ('no_pool_well_septic', models.NullBooleanField()),
                ('local_school_quality', models.PositiveIntegerField(blank=True, null=True)),
                ('rx_date_listed', models.CharField(blank=True, max_length=280, null=True)),
                ('garage_size', models.PositiveIntegerField(blank=True, null=True)),
                ('mls_listing_id', models.BigIntegerField(blank=True, null=True)),
                ('img_path_header', models.CharField(blank=True, max_length=280, null=True)),
                ('img_paths_gallery', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='SoldProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address_1', models.CharField(max_length=191)),
                ('street_address_2', models.CharField(blank=True, max_length=191, null=True)),
                ('city', models.CharField(max_length=191)),
                ('state', models.CharField(max_length=191)),
                ('zip_code', models.CharField(max_length=15)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('hc_slug', models.SlugField(max_length=191, unique=True)),
                ('lowercase_slug', models.SlugField(max_length=191)),
                ('sold_price', models.BigIntegerField(blank=True, null=True)),
                ('num_bedrooms', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('num_bathrooms', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('building_area_sq_ft', models.PositiveIntegerField(blank=True, null=True)),
                ('home_type', models.CharField(blank=True, max_length=280, null=True)),
                ('sale_price_history', models.TextField(blank=True, null=True)),
                ('certified_max_bid', models.BigIntegerField(blank=True, null=True)),
                ('certified_max_bid_created_at', models.DateTimeField(blank=True, null=True)),
                ('house_canary_avm', models.BigIntegerField(blank=True, null=True)),
                ('red_bell_ave', models.BigIntegerField(blank=True, null=True)),
                ('red_bell_ar_bpo', models.BigIntegerField(blank=True, null=True)),
                ('red_bell_bpo', models.BigIntegerField(blank=True, null=True)),
                ('num_floors', models.PositiveIntegerField(blank=True, null=True)),
                ('rx_num_half_bath', models.PositiveIntegerField(blank=True, null=True)),
                ('rx_num_full_bath', models.PositiveIntegerField(blank=True, null=True)),
                ('year_built', models.PositiveIntegerField(blank=True, null=True)),
                ('listing_status', models.CharField(blank=True, max_length=280, null=True)),
                ('flooring', models.CharField(blank=True, max_length=280, null=True)),
                ('interior_features', models.CharField(blank=True, max_length=280, null=True)),
                ('remax_url', models.CharField(blank=True, max_length=500, null=True)),
                ('subdivision', models.CharField(blank=True, max_length=280, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_foreclosure', models.NullBooleanField()),
                ('has_septic', models.NullBooleanField()),
                ('has_pool', models.NullBooleanField()),
                ('has_established_subdivision', models.NullBooleanField()),
                ('has_well', models.NullBooleanField()),
                ('has_garage', models.NullBooleanField()),
                ('no_pool_well_septic', models.NullBooleanField()),
                ('local_school_quality', models.PositiveIntegerField(blank=True, null=True)),
                ('rx_date_listed', models.CharField(blank=True, max_length=280, null=True)),
                ('garage_size', models.PositiveIntegerField(blank=True, null=True)),
                ('mls_listing_id', models.BigIntegerField(blank=True, null=True)),
                ('img_path_header', models.CharField(blank=True, max_length=280, null=True)),
                ('img_paths_gallery', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
    ]
