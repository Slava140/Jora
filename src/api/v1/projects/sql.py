from sqlalchemy import text

class ProjectSQL:
    @staticmethod
    def get_many(user_id: int, limit: int, offset: int):
        return text("""
                    select distinct p.*
                    from projects p
                            left join tasks t on t.project_id = p.id
                    where not p.is_archived
                      and (not t.is_archived or t.is_archived is null)
                      and (p.owner_id = :user_id or t.assignee_id = :user_id)
                    limit :limit
                    offset :offset""").bindparams(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )

    @staticmethod
    def get_users(project_id: int):
        return text("""
                    with cte_users as (select p.owner_id as user_id
                                       from projects p
                                                left join tasks t on p.id = t.project_id
                                       where p.id = :project_id

                                       union

                                       select t.assignee_id
                                       from projects p
                                                left join tasks t on p.id = t.project_id
                                       where p.id = :project_id

                                       union

                                       select t.author_id
                                       from projects p
                                                left join tasks t on p.id = t.project_id
                                       where p.id = :project_id)

                    select u.*
                    from cte_users cte
                        inner join users u on u.id = cte.user_id
                    where cte.user_id is not null""").bindparams(
            project_id=project_id,
        )