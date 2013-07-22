#!/usr/bin/python

import unittest
from datetime import datetime, timedelta

from plotwattapi import Plotwatt, PlotwattError

class TestDisagDayGeneration(unittest.TestCase):
    def setUp(self):
        self.pw = Plotwatt(2517, "3b0f9e9a9d98137c")
        
        # clear any old meters
        for meter_id in self.pw.list_meters() :
            self.pw.delete_meter(meter_id)
    
    def test_list_and_create_meters(self):
        assert self.pw.list_meters() == []
        self.pw.create_meters(1)
        assert len(self.pw.list_meters()) == 1
    
    def test_push_readings(self):
        new_meter_ids = self.pw.create_meters(1)
        meter_id = self.pw.list_meters()[0]
        
        # testing the return value of create_meters against the return value of list_meters
        assert meter_id == new_meter_ids[0]
        assert len(new_meter_ids) == 1
        
        now = datetime.now()
        second = seconds = timedelta(seconds=1)
        self.pw.push_readings(meter_id, [1, 2, 3], [now, now + 1*second, now + 2*second])

        # overwrite old readings
        self.pw.push_readings(meter_id, [4, 5, 6], [now, now + 1*second, now + 2*second])

    def test_push_invalid_readings(self):
        self.pw.create_meters(1)
        meter_id = self.pw.list_meters()[0]
        
        now = datetime.now() + timedelta(days = 2)
        second = seconds = timedelta(seconds=1)
        try :
            self.pw.push_readings(meter_id, [1, 2, 3], [now, now + 1*second, now + 2*second])
            assert 'the previous line should have raised an error'
        except PlotwattError, e:
            assert 'Unprocessable' in str(e)
    def test_push_readings_valid_or_invalid(self):
      data = "70363,1.007,1258826400,70363,1.0,1258826460,70363,1.006,1258826520,70363,1.009,1258826580,70363,1.001,1258826640,70363,1.007,1258826700,70363,0.997,1258826760,70363,1.003,1258826820,70363,1.001,1258826880,70363,1.007,1258826940,70363,1.004,1258827000,70363,1.0,1258827060,70363,1.004,1258827120,70363,0.987,1258827180,70363,0.949,1258827240,70363,0.936,1258827300,70363,0.929,1258827360,70363,0.929,1258827420,70363,0.933,1258827480,70363,0.932,1258827540,70363,0.922,1258827600,70363,0.879,1258827660,70363,0.878,1258827720,70363,0.876,1258827780,70363,0.854,1258827840,70363,0.802,1258827900,70363,0.792,1258827960,70363,0.792,1258828020,70363,0.798,1258828080,70363,0.81,1258828140,70363,0.793,1258828200,70363,0.789,1258828260,70363,0.855,1258828320,70363,0.907,1258828380,70363,0.897,1258828440,70363,0.901,1258828500,70363,1.084,1258828560,70363,1.08,1258828620,70363,1.11,1258828680,70363,1.08,1258828740,70363,1.083,1258828800,70363,1.082,1258828860,70363,1.084,1258828920,70363,1.121,1258828980,70363,1.193,1258829040,70363,1.263,1258829100,70363,1.33,1258829160,70363,1.325,1258829220,70363,1.901,1258829280,70363,3.037,1258829340,70363,2.964,1258829400,70363,2.888,1258829460,70363,2.735,1258829520,70363,1.247,1258829580,70363,1.232,1258829640,70363,1.169,1258829700,70363,1.799,1258829760,70363,1.832,1258829820,70363,1.163,1258829880,70363,1.161,1258829940"
      res = self.pw._request(self.pw.push_readings_url, data)
      assert res
      self.assertTrue(True)

def main() :
    unittest.main()

if __name__ == '__main__':
    main()
