# schedule-generator
Given a list of courses, every 'top-level' schedule will be generated and displayed.
From each top-level schedule, remove any undesired courses to end up with smaller, more realistic schedules.

[Here's a link to the website](https://zyrrus.pythonanywhere.com/)

---

### Example Data
Here's some example data to paste after the `/editor/` part of the url:  

[{"name":"CSC 2362","start":"15:00","end":"16:20","days":["M", "W"]},{"name":"CSC 3200","start":"10:30","end":"11:20","days":["W"]},{"name":"CSC 3380","start":"16:30","end":"17:50","days":["T", "Th"]},{"name":"CSC 4330","start":"15:00","end":"16:20","days":["T", "Th"]},{"name":"CSC 3501","start":"13:30","end":"14:50","days":["T", "Th"]},{"name":"CSC 3730","start":"09:00","end":"10:20","days":["T", "Th"]},{"name":"CSC 4101","start":"12:00","end":"13:20","days":["M", "W"]},{"name":"CSC 4103","start":"13:30","end":"14:50","days":["M", "W"]},{"name":"CSC 4444","start":"15:30","end":"16:50","days":["M", "W"]},{"name":"MATH 2060","start":"12:30","end":"13:20","days":["T", "Th"]},{"name":"MATH 4020","start":"13:30","end":"14:50","days":["T", "Th"]},{"name":"MATH 4031","start":"09:30","end":"10:20","days":["M", "W", "F"]},{"name":"MATH 4065","start":"10:30","end":"11:50","days":["T", "Th"]},{"name":"MATH 4153","start":"15:00","end":"16:20","days":["T", "Th"]},{"name":"MATH 4200","start":"08:30","end":"09:20","days":["M", "W", "F"]},
