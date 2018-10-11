#
# Copyright 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Module for ebs data generation."""
from random import choice, uniform

from nise.generators.aws.aws_generator import AWSGenerator


class EBSGenerator(AWSGenerator):
    """Generator for EBS data."""

    STORAGE = (
        ('Hundreds', '40 - 200', '40 - 90 MB/sec', '1 TiB',
         'HDD-backed', 'Magnetic'),
        ('3000 for volumes <= 1 TiB', '10000', '160 MB/sec',
         '16 TiB', 'SSD-backed', 'General Purpose'),
    )

    def _get_storage(self):
        """Get storage data."""
        return choice(self.STORAGE)

    # pylint: disable=too-many-locals
    def _update_data(self, row, start, end):
        """Update data with generator specific data."""
        row = self._add_common_usage_info(row, start, end)

        rate = round(uniform(0.02, 0.16), 3)
        amount = uniform(0.2, 300.99)
        cost = amount * rate
        location, aws_region, _, storage_region = self._get_location()
        description = '${} per GB-Month of snapshot data stored - {}'.format(rate, location)
        burst, max_iops, max_thru, max_vol_size, vol_backed, vol_type = \
            self._get_storage()

        row['lineItem/ProductCode'] = 'AmazonEC2'
        row['lineItem/UsageType'] = '{}:VolumeUsage'.format(storage_region)
        row['lineItem/Operation'] = 'CreateVolume'
        row['lineItem/ResourceId'] = 'vol-{}'.format(self.fake.ean8())  # pylint: disable=no-member
        row['lineItem/UsageAmount'] = str(amount)
        row['lineItem/CurrencyCode'] = 'USD'
        row['lineItem/UnblendedRate'] = str(rate)
        row['lineItem/UnblendedCost'] = str(cost)
        row['lineItem/BlendedRate'] = str(rate)
        row['lineItem/BlendedCost'] = str(cost)
        row['lineItem/LineItemDescription'] = description
        row['product/ProductName'] = 'Amazon Elastic Compute Cloud'
        row['product/location'] = location
        row['product/locationType'] = 'AWS Region'
        row['product/maxIopsBurstPerformance'] = burst
        row['product/maxIopsvolume'] = max_iops
        row['product/maxThroughputvolume'] = max_thru
        row['product/maxVolumeSize'] = max_vol_size
        row['product/productFamily'] = 'Storage'
        row['product/region'] = aws_region
        row['product/servicecode'] = 'AmazonEC2'
        row['product/sku'] = self.fake.pystr(min_chars=12, max_chars=12).upper()  # pylint: disable=no-member
        row['product/storageMedia'] = vol_backed
        row['product/usagetype'] = '{}:VolumeUsage'.format(storage_region)
        row['product/volumeType'] = vol_type
        row['pricing/publicOnDemandCost'] = str(cost)
        row['pricing/publicOnDemandRate'] = str(rate)
        row['pricing/term'] = 'OnDemand'
        row['pricing/unit'] = 'GB-Mo'
        return row

    def generate_data(self):
        """Responsibile for generating data."""
        data = self._generate_hourly_data()
        return data