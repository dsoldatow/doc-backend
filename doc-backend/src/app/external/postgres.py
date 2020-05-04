import asyncpg


class PostgresEngine:
    """Соединение с БД Postgres."""

    def __init__(self):
        """Инициализация полей."""
        self._connect_data: dict = None
        self.pool: asyncpg.pool.Pool = None

    async def exec_(self, query, *args):
        async with self.pool.acquire() as conn:
            records = await conn.fetch(query, *args)
            values = [dict(record) for record in records]

        return values

    async def setup(self, connect_data):  # noqa: D102
        self._connect_data = connect_data  # noqa: Z112
        self.pool = await self._make_connection_pool()

    async def _make_connection_pool(self):
        # if self._connect_data is None:
        # raise ServiceError('No connection data is provided')
        return await asyncpg.create_pool(
            host=self._connect_data['host'],
            port=self._connect_data['port'],
            user=self._connect_data['username'],
            password=self._connect_data['password'],
            database=self._connect_data['name'],
            min_size=self._connect_data['min_con'],
            max_size=self._connect_data['max_con'],
        )

    async def close(self):
        await self.pool.close()

    async def check_connection_status(self):
        result_code = 1
        if self.pool is None:
            return -1
        try:
            async with self.pool.acquire() as conn:
                result_code = await conn.fetchval('SELECT 0')
        except Exception as error:
            pass
            # log.error(f'Error when checking status connection: {error}')
        return result_code  # noqa: Z331

    async def reconnect(self):
        # log.info('Try to reconnect')
        self.pool = await self._make_connection_pool()
        cur_status = await self.check_connection_status()
        # log.info(f'Reconnected to database. Status of new connection {cur_status}')
        return cur_status
