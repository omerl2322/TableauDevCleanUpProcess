select workbooks.name as workbook_name,
        workbooks.luid as workbook_id,
        su.email as owner_email,
        tasks.luid as task_id
from workbooks join users u on workbooks.owner_id = u.id
join system_users su on u.system_user_id = su.id
left join tasks on workbooks.id = tasks.obj_id
where last_published_at <= current_date-7*X 