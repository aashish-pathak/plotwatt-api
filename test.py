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
      new_meter_ids = self.pw.create_meters(1)
      meter_id = self.pw.list_meters()[0]
      
      assert meter_id == new_meter_ids[0]
      assert len(new_meter_ids) == 1
 
      try :
        self.pw.push_readings(meter_id, [1.007, 1.0, 1.006, 1.009, 1.001, 1.007, 0.997, 1.003, 1.001, 1.007, 1.004, 1.0, 1.004, 0.987, 0.949, 0.936, 0.929, 0.929, 0.933, 0.932, 0.922, 0.879, 0.878, 0.876, 0.854, 0.802, 0.792, 0.792, 0.798, 0.81, 0.793, 0.789, 0.855, 0.907, 0.897, 0.901, 1.084, 1.08, 1.11, 1.08, 1.083, 1.082, 1.084, 1.121, 1.193, 1.263, 1.33, 1.325, 1.901, 3.037, 2.964, 2.888, 2.735, 1.247, 1.232, 1.169, 1.799, 1.832, 1.163, 1.161], [1258826400, 1258826460, 1258826520, 1258826580, 1258826640, 1258826700, 1258826760, 1258826820, 1258826880, 1258826940, 1258827000, 1258827060, 1258827120, 1258827180, 1258827240, 1258827300, 1258827360, 1258827420, 1258827480, 1258827540, 1258827600, 1258827660, 1258827720, 1258827780, 1258827840, 1258827900, 1258827960, 1258828020, 1258828080, 1258828140, 1258828200, 1258828260, 1258828320, 1258828380, 1258828440, 1258828500, 1258828560, 1258828620, 1258828680, 1258828740, 1258828800, 1258828860, 1258828920, 1258828980, 1258829040, 1258829100, 1258829160, 1258829220, 1258829280, 1258829340, 1258829400, 1258829460, 1258829520, 1258829580, 1258829640, 1258829700, 1258829760, 1258829820, 1258829880, 1258829940])        
      except PlotwattError, e:
        assert 'Unprocessable' in str(e)

def main() :
    unittest.main()

if __name__ == '__main__':
    main()
