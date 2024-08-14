# BSD 3-Clause License

# Copyright (c) 2024, The Regents of the University of California (Regents)
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
sys.path.append('../src')
sys.path.append('./src')
from sdtp import RowTable
from sdtp import SDML_STRING, SDML_NUMBER, SDML_DATE, SDML_TIME_OF_DAY, SDML_DATETIME, SDML_BOOLEAN

# Tables used in test_table_server
test1 = RowTable([
  {"name": "column1", "type": SDML_STRING},
  {"name": "column2", "type": SDML_NUMBER}
], [
  ["Tom", 23],
  ["Misha", 37],
  ["Karen", 38],
  ["Vijay", 27],
  ["Alexandra", 25],
  ["Hitomi", 45]
])


test2 = RowTable([
  {"name": "column1", "type": SDML_STRING},
  {"name": "column2", "type": SDML_NUMBER}
], [
  ["Tammy", 48],
  ["Sujata", 36],
  ["Karen", 38],
  ["Tori", 27],
  ["Alexandra", 25],
  ["Hitomi", 45]
])


test3 = RowTable([
  { "name": "name", "type": SDML_STRING },
  { "name": "age", "type": SDML_NUMBER },
  { "name": "date", "type": SDML_DATE }, 
  { "name": "time", "type": SDML_TIME_OF_DAY },
  { "name": "datetime", "type": SDML_DATETIME },
  { "name": "boolean", "type": SDML_BOOLEAN }
], [
  [ "Pearla", 64, "2020-09-24", "11:24:55", "2020-09-24T11:24:55", True ],
  [ "Karleen", 78, "2011-12-09", "13:40:27", "2011-12-09T13:40:27", True ],
  [ "Bathsheba", 79, "2010-08-07", "23:44:12", "2010-08-07T23:44:12", True ],
  [ "Casi", 13, "2021-10-17", "17:13:02", "2021-10-17T17:13:02", True ],
  [ "Gusti", 28, "2013-07-04", "10:48:05", "2013-07-04T10:48:05", False ],
  [ "Anastassia", 70, "2022-07-08", "17:12:00", "2022-07-08T17:12:00", False ],
  [ "Nonah", 79, "2013-06-20", "00:53:03", "2013-06-20T00:53:03", True ],
  [ "Janine", 87, "2019-12-17", "12:19:43", "2019-12-17T12:19:43", False ],
  [ "Nicki", 31, "2005-07-25", "07:33:45", "2005-07-25T07:33:45", True ],
  [ "Noemi", 7, "2000-12-26", "01:06:34", "2000-12-26T01:06:34", True ],
  [ "Vivyanne", 46, "2003-02-23", "14:41:46", "2003-02-23T14:41:46", False ],
  [ "Jeanne", 51, "2007-11-11", "20:21:12", "2007-11-11T20:21:12", True ],
  [ "Carina", 29, "2017-05-23", "20:55:33", "2017-05-23T20:55:33", True ],
  [ "Ivy", 13, "2022-10-24", "12:36:15", "2022-10-24T12:36:15", True ],
  [ "Jenine", 43, "2017-07-01", "10:57:56", "2017-07-01T10:57:56", True ],
  [ "Tandie", 17, "2010-06-28", "06:38:17", "2010-06-28T06:38:17", True ],
  [ "Abbe", 83, "2009-07-23", "06:58:34", "2009-07-23T06:58:34", False ],
  [ "Laney", 29, "2005-06-08", "04:07:44", "2005-06-08T04:07:44", True ],
  [ "Shandeigh", 46, "2001-01-07", "17:38:14", "2001-01-07T17:38:14", True ],
  [ "Aarika", 55, "2005-05-27", "17:35:48", "2005-05-27T17:35:48", True ],
  [ "Caria", 60, "2010-03-19", "04:40:59", "2010-03-19T04:40:59", False ],
  [ "Jorrie", 37, "2013-10-12", "15:09:38", "2013-10-12T15:09:38", True ],
  [ "Maisey", 50, "2007-10-09", "21:23:29", "2007-10-09T21:23:29", False ],
  [ "Shani", 9, "2006-11-11", "21:59:19", "2006-11-11T21:59:19", False ],
  [ "Casi", 57, "2018-03-11", "00:13:53", "2018-03-11T00:13:53", True ],
  [ "Ashley", 88, "2016-12-14", "17:30:14", "2016-12-14T17:30:14", False ],
  [ "Roselia", 74, "2000-07-05", "14:40:38", "2000-07-05T14:40:38", True ],
  [ "Petronia", 47, "2015-03-05", "22:40:39", "2015-03-05T22:40:39", True ],
  [ "Brandice", 67, "2004-08-31", "03:13:27", "2004-08-31T03:13:27", True ],
  [ "Debi", 42, "2001-04-14", "08:19:40", "2001-04-14T08:19:40", False ],
  [ "Andee", 82, "2006-02-02", "20:24:01", "2006-02-02T20:24:01", True ],
  [ "Teodora", 63, "2021-10-02", "22:20:04", "2021-10-02T22:20:04", True ],
  [ "Neysa", 79, "2014-01-06", "17:42:39", "2014-01-06T17:42:39", True ],
  [ "Beverley", 81, "2003-12-17", "23:15:20", "2003-12-17T23:15:20", True ],
  [ "Rey", 34, "2019-07-26", "03:20:46", "2019-07-26T03:20:46", False ],
  [ "Brittni", 77, "2008-04-19", "20:25:31", "2008-04-19T20:25:31", False ],
  [ "Rheba", 80, "2019-06-08", "16:42:31", "2019-06-08T16:42:31", True ],
  [ "Jeanna", 51, "2010-10-02", "22:15:59", "2010-10-02T22:15:59", True ],
  [ "Lyssa", 68, "2021-06-11", "00:37:44", "2021-06-11T00:37:44", False ],
  [ "Elayne", 61, "2015-06-16", "01:46:17", "2015-06-16T01:46:17", True ],
  [ "Magdalene", 72, "2005-04-01", "00:24:01", "2005-04-01T00:24:01", False ],
  [ "Violante", 71, "2004-04-21", "18:54:22", "2004-04-21T18:54:22", False ],
  [ "Netta", 59, "2021-02-10", "03:24:24", "2021-02-10T03:24:24", False ],
  [ "Virginia", 55, "2019-09-28", "22:17:08", "2019-09-28T22:17:08", True ],
  [ "Natalie", 31, "2020-04-02", "22:17:17", "2020-04-02T22:17:17", False ],
  [ "Mildred", 57, "2004-09-28", "18:28:49", "2004-09-28T18:28:49", False ],
  [ "Ophelia", 31, "2008-04-22", "09:15:21", "2008-04-22T09:15:21", True ],
  [ "Alma", 66, "2001-01-22", "16:55:20", "2001-01-22T16:55:20", True ],
  [ "Lettie", 91, "2014-08-15", "18:14:10", "2014-08-15T18:14:10", True ],
  [ "Catherina", 45, "2016-01-18", "00:11:37", "2016-01-18T00:11:37", False ],
  [ "Philipa", 58, "2014-04-29", "00:44:46", "2014-04-29T00:44:46", True ],
  [ "Marget", 59, "2002-06-11", "10:09:12", "2002-06-11T10:09:12", True ],
  [ "Karol", 77, "2015-10-28", "10:43:15", "2015-10-28T10:43:15", False ],
  [ "Berget", 15, "2020-07-22", "11:16:57", "2020-07-22T11:16:57", False ],
  [ "Doloritas", 42, "2015-05-17", "14:25:31", "2015-05-17T14:25:31", False ],
  [ "Kessia", 39, "2019-03-23", "14:06:35", "2019-03-23T14:06:35", True ],
  [ "Jaynell", 92, "2023-01-24", "16:14:38", "2023-01-24T16:14:38", True ],
  [ "Bethanne", 82, "2017-07-22", "08:58:06", "2017-07-22T08:58:06", False ],
  [ "Mildred", 90, "2021-04-21", "23:15:27", "2021-04-21T23:15:27", True ],
  [ "Gustie", 77, "2006-01-04", "10:07:34", "2006-01-04T10:07:34", True ],
  [ "Irina", 60, "2020-02-11", "04:39:45", "2020-02-11T04:39:45", True ],
  [ "Felipa", 20, "2018-12-01", "20:03:52", "2018-12-01T20:03:52", True ],
  [ "Charlean", 23, "2021-06-22", "21:46:58", "2021-06-22T21:46:58", False ],
  [ "Jaquelin", 31, "2001-11-28", "13:24:37", "2001-11-28T13:24:37", True ],
  [ "Isadora", 83, "2015-04-05", "01:56:52", "2015-04-05T01:56:52", False ],
  [ "Jelene", 34, "2010-12-10", "08:09:09", "2010-12-10T08:09:09", False ],
  [ "Benedicta", 89, "2011-03-27", "10:51:03", "2011-03-27T10:51:03", False ],
  [ "Piper", 83, "2012-10-13", "19:19:52", "2012-10-13T19:19:52", True ],
  [ "Almeria", 55, "2003-05-29", "12:03:04", "2003-05-29T12:03:04", False ],
  [ "Editha", 38, "2016-07-23", "06:11:21", "2016-07-23T06:11:21", False ],
  [ "Deena", 45, "2004-05-23", "16:01:11", "2004-05-23T16:01:11", False ],
  [ "Celestyn", 51, "2022-05-28", "07:09:58", "2022-05-28T07:09:58", False ],
  [ "Betsy", 10, "2007-08-05", "16:09:03", "2007-08-05T16:09:03", True ],
  [ "Georgianna", 90, "2007-10-03", "14:07:44", "2007-10-03T14:07:44", False ],
  [ "Jacklin", 55, "2013-10-10", "17:53:11", "2013-10-10T17:53:11", True ],
  [ "Georgiana", 85, "2017-12-17", "23:35:29", "2017-12-17T23:35:29", True ],
  [ "Robby", 38, "2010-12-24", "11:29:53", "2010-12-24T11:29:53", True ],
  [ "Emmalyn", 53, "2003-08-27", "15:53:20", "2003-08-27T15:53:20", True ],
  [ "Robinett", 75, "2004-03-05", "08:06:15", "2004-03-05T08:06:15", False ],
  [ "Nickie", 11, "2016-08-27", "09:23:28", "2016-08-27T09:23:28", True ],
  [ "Jo-Ann", 74, "2003-04-09", "21:35:58", "2003-04-09T21:35:58", True ],
  [ "Rosita", 80, "2013-10-15", "23:11:13", "2013-10-15T23:11:13", False ],
  [ "Ingrid", 52, "2005-07-26", "20:21:17", "2005-07-26T20:21:17", True ],
  [ "Erminie", 31, "2014-05-21", "17:47:27", "2014-05-21T17:47:27", False ],
  [ "Tami", 69, "2000-03-01", "19:58:11", "2000-03-01T19:58:11", False ],
  [ "Meg", 25, "2018-03-10", "22:28:52", "2018-03-10T22:28:52", False ],
  [ "Devan", 76, "2017-11-19", "15:24:08", "2017-11-19T15:24:08", False ],
  [ "Annaliese", 63, "2014-08-13", "12:33:26", "2014-08-13T12:33:26", False ],
  [ "Ginevra", 11, "2006-07-11", "14:29:36", "2006-07-11T14:29:36", False ],
  [ "Wilmette", 77, "2010-04-24", "03:35:48", "2010-04-24T03:35:48", False ],
  [ "Imogen", 33, "2010-09-23", "18:35:37", "2010-09-23T18:35:37", True ],
  [ "Melony", 18, "2022-04-01", "11:52:44", "2022-04-01T11:52:44", True ],
  [ "Kalli", 19, "2020-06-29", "21:15:48", "2020-06-29T21:15:48", False ],
  [ "Tessy", 53, "2003-09-09", "07:39:00", "2003-09-09T07:39:00", False ],
  [ "Lesly", 64, "2008-01-04", "04:34:48", "2008-01-04T04:34:48", True ],
  [ "Deedee", 11, "2019-09-03", "05:20:58", "2019-09-03T05:20:58", True ],
  [ "Mellisent", 17, "2004-12-14", "18:36:56", "2004-12-14T18:36:56", False ],
  [ "Perl", 50, "2016-05-26", "00:16:33", "2016-05-26T00:16:33", True ],
  [ "Milzie", 92, "2001-03-05", "07:27:51", "2001-03-05T07:27:51", True ],
  [ "Allegra", 55, "2013-10-03", "00:50:14", "2013-10-03T00:50:14", False ]
])


test_tables = [
  {"name": "test1", "table": test1},
  {"name": "test2", "table": test2},
  {"name": "test3", "table": test3}
]