import re


def requests_per_day(log):
    requests = re.findall(r'\d{4}-\d{2}-\d{2}', log)
    dates = {}
    for item in requests:
        if item in dates:
            dates[item] = dates[item] + 1
        else:
            dates[item] = 1
    return dates


def ips_set(log):
    return set(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", log))


str = """Started GET "/posts/44" for 351.254.129.87 at 2016-02-28 11:34:11 +0200
Processing by PostsController#show as HTML
  Parameters: {"id"=>"44"}
Redirected to http://2015.fmi.py-bg.net/topics/1/replies/44
Completed 302 Found in 4ms (ActiveRecord: 1.2ms)
Started GET "/topics/1/replies/44" for 51.254.129.87 at 2016-02-28 11:34:13 +0200
Processing by RepliesController#show as HTML
  Parameters: {"topic_id"=>"1", "id"=>"44"}
Redirected to http://2015.fmi.py-bg.net/topics/1?page=2#reply_44
Completed 302 Found in 7ms (ActiveRecord: 1.6ms)
Started GET "/topics/1?page=2" for 51.254.129.87 at 2016-02-28 11:34:14 +0200
Processing by TopicsController#show as HTML
  Parameters: {"page"=>"2", "id"=>"1"}
  Rendered common/_contribution.html.haml (7.0ms)
  Rendered common/_contribution.html.haml (5.7ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.5ms)
  Rendered common/_contribution.html.haml (5.5ms)
  Rendered common/_contribution.html.haml (5.3ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.5ms)
  Rendered common/_contribution.html.haml (5.7ms)
  Rendered common/_contribution.html.haml (5.2ms)
  Rendered common/_contribution.html.haml (5.3ms)
  Rendered common/_contribution.html.haml (5.1ms)
  Rendered common/_contribution.html.haml (5.1ms)
  Rendered common/_contribution.html.haml (5.4ms)
  Rendered common/_contribution.html.haml (5.1ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.7ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.6ms)
  Rendered common/_contribution.html.haml (5.5ms)
  Rendered common/_contribution.html.haml (5.7ms)
  Rendered common/_contribution.html.haml (5.2ms)
  Rendered common/_contribution.html.haml (5.7ms)
  Rendered common/_contribution.html.haml (5.2ms)
  Rendered common/_contribution.html.haml (5.5ms)
  Rendered common/_contribution.html.haml (5.7ms)
  Rendered common/_contribution.html.haml (5.5ms)
  Rendered topics/show.html.haml within layouts/application (186.3ms)
  Rendered common/_tip_of_the_day.html.haml (0.5ms)
  Rendered common/_google_analytics.html.haml (0.4ms)
Completed 200 OK in 199ms (Views: 175.8ms | ActiveRecord: 19.9ms)
Started GET "/leaderboard" for 212.25.142.226 at 2016-04-21 04:45:29 +0300
Processing by LeaderboardsController#show as HTML
  Rendered leaderboards/show.html.haml within layouts/application (138.0ms)
  Rendered common/_tip_of_the_day.html.haml (0.5ms)
  Rendered common/_google_analytics.html.haml (0.3ms)
Completed 200 OK in 290ms (Views: 170.9ms | ActiveRecord: 107.0ms)
Started GET "/leaderboard" for 212.25.142.226 at 2016-04-21 04:45:29 +0300
Processing by LeaderboardsController#show as HTML
  Rendered leaderboards/show.html.haml within layouts/application (138.0ms)
  Rendered common/_tip_of_the_day.html.haml (0.5ms)
  Rendered common/_google_analytics.html.haml (0.3ms)
Completed 200 OK in 290ms (Views: 170.9ms | ActiveRecord: 107.0ms)
Started GET "/leaderboard" for 66.249.66.41 at 2016-04-22 04:45:29 +0300
Processing by LeaderboardsController#show as HTML
  Rendered leaderboards/show.html.haml within layouts/application (138.0ms)
  Rendered common/_tip_of_the_day.html.haml (0.5ms)
  Rendered common/_google_analytics.html.haml (0.3ms)
Completed 200 OK in 290ms (Views: 170.9ms | ActiveRecord: 107.0ms)"""

print(requests_per_day(str))
print(ips_set(str))