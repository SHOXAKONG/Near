with category_stats as (select category_id as category_id, c.name as category_name, count(*) as search_count
                        from history_searchhistory h
                                 join category c on h.category_id = c.id
                        group by category_id, c.name
                        order by search_count desc),

     users_stats as (select u.id as user_id, u.first_name, count(h.id) as total_searches
                     from users_users u
                              LEFT join history_searchhistory h on u.id = h.user_id
                     group by u.id, u.first_name
                     HAVING count(h.id) > 0
                     order by total_searches desc),


     daily_stats as (select DATE_TRUNC('day', created_at) ::date as date, count (*) as search_count
from history_searchhistory
group by date
order by date asc),
    monthly_stats as (
select DATE_TRUNC('month', created_at):: date as month, count (DISTINCT u.id) as user_registrations, count (h.id) as category_searches
from users_users u
    LEFT join history_searchhistory h
on u.id = h.user_id
group by month
order by month asc),
    full_search_history as (
select h.id, u.first_name as user, c.name as category, h.latitude, h.longitude, h.created_at
from history_searchhistory h
    join users_users u
on h.user_id = u.id
    join category c on h.category_id = c.id
order by h.created_at desc)

select 'Category Stats' as section, to_json(category_stats.*) as data
from category_stats
union all
select 'Users Stats' as section, to_json(users_stats.*) as data
from users_stats
union all
select 'Daily Stats' as section, to_json(daily_stats.*) as data
from daily_stats
union all
select 'Monthly Stats' as section, to_json(monthly_stats.*) as data
from monthly_stats
union all
select 'Full History Search' as section, to_json(full_search_history.*) as data
from full_search_history;


with category_stats as (select h.category_id as category_id,
                               c.name        as category_name,
                               count(*)      as search_count
                        from history_searchhistory h
                                 join category c on h.category_id = c.id
                        group by h.category_id, c.name
                        order by search_count desc),

     users_stats as (select u.id        as user_id,
                            u.first_name,
                            count(h.id) as total_searches
                     from users_users u
                              left join history_searchhistory h on u.id = h.user_id
                     group by u.id, u.first_name
                     having count(h.id) > 0
                     order by total_searches desc),

     daily_stats as (select date_trunc('day', created_at) ::date as date, count (*) as search_count
from history_searchhistory
group by date
order by date asc
    ),
    monthly_stats as (
select
    date_trunc('month', created_at):: date as month, count (distinct u.id) as user_registrations, count (h.id) as category_searches
from users_users u
    left join history_searchhistory h
on u.id = h.user_id
group by month
order by month asc
    ),
    full_search_history as (
select
    h.id, u.first_name as user, c.name as category, h.latitude, h.longitude, h.created_at
from history_searchhistory h
    join users_users u
on h.user_id = u.id
    join category c on h.category_id = c.id
order by h.created_at desc
    )

select 'category stats' as section,
    category_id::text as col1,
    category_name as col2,
    search_count::text as col3,
    null as col4,
    null as col5,
    null as col6
from category_stats

union all

select 'users stats' as section,
    user_id::text as col1,
    first_name as col2,
    total_searches::text as col3,
    null as col4,
    null as col5,
    null as col6
from users_stats

union all

select 'daily stats' as section,
    date::text as col1,
    null as col2,
    search_count::text as col3,
    null as col4,
    null as col5,
    null as col6
from daily_stats

union all

select 'monthly stats' as section,
    month::text as col1,
    user_registrations::text as col2,
    category_searches::text as col3,
    null as col4,
    null as col5,
    null as col6
from monthly_stats

union all

select 'full history search' as section,
    id::text as col1,
    "user" as col2,
    category as col3,
    latitude::text as col4,
    longitude::text as col5,
    created_at::text as col6
from full_search_history;