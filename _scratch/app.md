# Team members availability app

There is a large team whose members are spread across multiple continents. (say Australia, China, USA).
I want to build an application which can do the following.

## Features

1. It stores all national and regional/state holidays.
2. It has access to information regarding which member works in which country and region.
3. It has the ability for each member to add their OOO (out of office) dates. (e.g vacations).
4. The app display page should give a calendar view with details of which team members are away on corresponding days.

### Important

1. all code should be inside app folder.
2. Use Python (flask) to build entire app.


### display page features:

1. i should see only those employees who are OOO (either by vacation or holidays)
2. For adding and removing out of office can we make this interactive .. to add .delete  directly in the calenear instead of another tab
3. calender out of office entries can be added or deleted.
4. There should be a history tab which will list all the operations by all members so that there is trace.


### Member and location information

Naga | Australia, NSW
Anuj | Australia, VIC
Teresa | Australia, WA
Xing | China, Shanghai
Hang | China, Shanghai
Jeffery | USA, California

### Calendar view

it should be like below 

member name 1 | OOO 
member name 2 | location (public holiday)


### Member and public holiday functionality

1. When i add new member, it should display following country options main top 10 economies in the world along with Australia.
2. IT should also give region/state/province as option to pick and it should populate these values.
3. once the member is added, it should check if the country and state is availabe in holidays .. if not then add national and regional holidays.
4. use holidays libarary from python to get the data for all of above