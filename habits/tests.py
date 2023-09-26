# Create your tests here.
from unittest.mock import patch

from rest_framework import status

from habits.models import Habit, PleasantHabit
from users.tests import UserModelTestCase


class HabitModelTestCase(UserModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Создание непубличного объекта Habit для тестового пользователя
        self.habit_object_1 = Habit.objects.create(
            habit_user=self.user_test,
            place='Дом',
            date_time='2023-09-24T20:00:00Z',
            action='Делать зарядку',
            interval='Ежедневно',
            execution_time='120',
            reward='Съесть шоколадку',
            is_published=False,
        )
        self.habit_object_1.save()

        # Создание публичного объекта Habit для тестового пользователя
        self.habit_object_1_public = Habit.objects.create(
            habit_user=self.user_test,
            place='Дом',
            date_time='2023-09-24T20:00:00Z',
            action='Делать зарядку',
            interval='Ежедневно',
            execution_time='120',
            reward='Съесть шоколадку',
            is_published=True,
        )
        self.habit_object_1_public.save()

        # Создание непубличного объекта Habit для второго пользователя
        self.habit_object_2 = Habit.objects.create(
            habit_user=self.user_2,
            place='Дом',
            date_time='2023-09-24T10:00:00Z',
            action='Делать зарядку',
            interval='Ежедневно',
            execution_time='120',
            reward='Съесть шоколадку',
            is_published=False,
        )
        self.habit_object_2.save()

        # Создание публичного объекта Habit для второго пользователя
        self.habit_object_2_public = Habit.objects.create(
            habit_user=self.user_2,
            place='Дом',
            date_time='2023-09-24T09:00:00Z',
            action='Делать зарядку',
            interval='Ежедневно',
            execution_time='120',
            reward='Съесть шоколадку',
            is_published=True,
        )
        self.habit_object_2_public.save()

        # Создание объекта PleasantHabit для тестового пользователя
        self.pleasant_habit_test = PleasantHabit.objects.create(
            habit_user=self.user_test,
            place='Дом',
            date_time='2023-09-24T18:00:00Z',
            action='Делать зарядку',
            execution_time='120',
            is_published=False,
        )
        self.pleasant_habit_test.save()

        # Создание непубличного объекта PleasantHabit для второго пользователя
        self.pleasant_habit_user_2_unpublished = PleasantHabit.objects.create(
            habit_user=self.user_2,
            place='Дом',
            date_time='2023-09-24T19:00:00Z',
            action='Делать зарядку',
            execution_time='120',
            is_published=False,
        )
        self.pleasant_habit_user_2_unpublished.save()

        # Создание публичного объекта PleasantHabit для второго пользователя
        self.pleasant_habit_user_2_published = PleasantHabit.objects.create(
            habit_user=self.user_2,
            place='Дом',
            date_time='2023-09-24T20:00:00Z',
            action='Делать зарядку',
            execution_time='120',
            is_published=True,
        )
        self.pleasant_habit_user_2_published.save()

        self.create_url = '/habits/create/'

        # Сырые данные для создания Habit
        self.raw_habit_data = {
            'habit_user': 'test@test.com',
            'place': 'Дом',
            'action': 'Делать зарядку',
            'interval': 'Ежедневно',
        }

    def tearDown(self) -> None:
        return super().tearDown()


class HabitCreateTestCase(HabitModelTestCase):

    def setUp(self) -> None:
        super().setUp()
        # Получение маршрутов
        self.create_url = '/habits/create/'

        # Сырые данные для создания Habit
        self.raw_habit_data = {
            'habit_user': self.user_test.email,
            'place': 'Дом',
            'action': 'Делать зарядку',
            'interval': 'Ежедневно',
        }

    def test_user_cannot_create_habit_without_authentication(self):
        """Пользователь не может создавать объекты без авторизации."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T21:00:00Z'
        self.raw_habit_data['execution_time'] = '120'
        self.raw_habit_data['reward'] = 'Лучший.'
        self.raw_habit_data['is_published'] = False

        # Количество привычек до создания
        self.assertTrue(
            Habit.objects.count() == 4
        )

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=None,
            format='json'
        )

        # Количество привычек после создания
        self.assertTrue(
            Habit.objects.count() == 4
        )

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_can_create_habit_with_reward(self):
        """Пользователь может создавать объекты модели Habit после авторизации, но необходимо указать ЛИБО 'reward',
        ЛИБО 'pleasant_habit'."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T23:00:00Z'
        self.raw_habit_data['execution_time'] = '120'
        self.raw_habit_data['reward'] = 'Лучший.'
        self.raw_habit_data['is_published'] = False

        # Количество привычек до создания
        self.assertTrue(
            Habit.objects.count() == 4
        )

        # Отключение отложенной задачи
        self.patcher = patch('habits.tasks.register_habit.delay')
        self.mock_task = self.patcher.start()

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Включение отложенной задачи
        self.patcher.stop()

        # Количество привычек после создания
        self.assertTrue(
            Habit.objects.count() == 5
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_user_cannot_create_habit_with_reward_and_pleasant_habit(self):
        """Пользователю при создании объекта Habit необходимо указать ЛИБО 'reward', ЛИБО 'pleasant_habit'."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T23:00:00Z'
        self.raw_habit_data['execution_time'] = '120'
        self.raw_habit_data['is_published'] = False

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'reward_or_pleasant_habit_fields': ["Необходимо указать ЛИБО 'reward', ЛИБО 'pleasant_habit'."]}
        )

    def test_user_can_create_habit_with_pleasant_habit(self):
        """Пользователь может создавать объекты модели Habit после авторизации, но необходимо указать ЛИБО 'reward',
        ЛИБО 'pleasant_habit'. При указании <pleasant_habit>, создателем объекта PleasantHabit должен быть создатель
        Habit или PleasantHabit должен быть публичным (is_published=True)."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T23:00:00Z'
        self.raw_habit_data['execution_time'] = '120'
        self.raw_habit_data['pleasant_habit'] = self.pleasant_habit_test.pk
        self.raw_habit_data['is_published'] = False

        # Количество привычек до создания
        self.assertTrue(
            Habit.objects.count() == 4
        )

        # Отключение отложенной задачи
        self.patcher = patch('habits.tasks.register_habit.delay')
        self.mock_task = self.patcher.start()

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Включение отложенной задачи
        self.patcher.stop()

        # Количество привычек после создания
        self.assertTrue(
            Habit.objects.count() == 5
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_user_cannot_create_habit_with_now_owner_pleasant_habit(self):
        """Пользователь не может создавать объекты модели Habit, если он не является создателем объекта PleasantHabit
        для поля <pleasant_habit>, а также если этот объект непубличный."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T23:00:00Z'
        self.raw_habit_data['execution_time'] = '120'
        self.raw_habit_data['pleasant_habit'] = self.pleasant_habit_user_2_unpublished.pk
        self.raw_habit_data['is_published'] = False

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'pleasant_habit': ['Вы можете добавлять только свою приятную привычку или доступную для всех.']}
        )

    def test_user_can_create_habit_with_public_pleasant_habit(self):
        """Пользователь может создавать объекты модели Habit с публичными PleasantHabit любых пользователей."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T23:00:00Z'
        self.raw_habit_data['execution_time'] = '120'
        self.raw_habit_data['pleasant_habit'] = self.pleasant_habit_user_2_published.pk
        self.raw_habit_data['is_published'] = False

        # Количество привычек до создания
        self.assertTrue(
            Habit.objects.count() == 4
        )

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Количество привычек после создания
        self.assertTrue(
            Habit.objects.count() == 5
        )

    def test_user_cannot_create_habit_with_execution_time_more_then_120(self):
        """Пользователь может создавать объекты модели Habit с полем <execution_time>, интервал которого должен быть
        в диапазоне от 0 до 120 секунд."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T23:00:00Z'
        self.raw_habit_data['execution_time'] = '130'
        self.raw_habit_data['reward'] = 'Лучший.'
        self.raw_habit_data['is_published'] = False

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )

    def test_user_cannot_create_habit_with_execution_time_less_then_or_equal_0(self):
        """Пользователь может создавать объекты модели Habit с полем <execution_time>, интервал которого должен быть
        в диапазоне от 0 до 120 секунд."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T23:00:00Z'
        self.raw_habit_data['execution_time'] = '0'
        self.raw_habit_data['reward'] = 'Лучший.'
        self.raw_habit_data['is_published'] = False

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )

    def test_user_cannot_create_habit_more_than_1_per_hour(self):
        """Пользователь может создавать объекты модели Habit не чаще, чем 1 в час."""

        # Дополнение сырых данных недостающими полями
        self.raw_habit_data['date_time'] = '2023-09-24T20:00:00Z'
        self.raw_habit_data['execution_time'] = '120'
        self.raw_habit_data['reward'] = 'Лучший.'
        self.raw_habit_data['is_published'] = False

        # POST-запрос на создание привычки
        response = self.client.post(
            self.create_url,
            self.raw_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'date_time': ['Для одного пользователя необходимо устанавливать привычку не чаще 1 в час.']}
        )


class HabitGetTestCase(HabitModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.get_habits_url = '/habits/'
        # маршрут до непубличного объекта Habit тестового пользователя
        self.get_detail_url = f'/habits/{self.habit_object_1.pk}/'

    def test_user_can_get_habits_correctly(self):
        """Авторизованный пользователь может просматривать только публичные и собственные привычки."""

        # GET-запрос на получение всех привычек
        response = self.client.get(
            self.get_habits_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка количества объектов в содержании ответа
        self.assertTrue(
            response.json().get('count') == 3
        )

        # Проверка количества объектов в базе данных
        self.assertTrue(
            Habit.objects.count() == 4
        )

    def test_user_cannot_get_habits_without_authentication(self):
        """Неавторизованные пользователи не имеют доступа к объектам модели Habit."""

        # GET-запрос на получение всех привычек
        response = self.client.get(
            self.get_habits_url,
            headers=None,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_can_get_detail_habit_correctly_owner(self):
        """Авторизованный пользователь может просматривать детализированную информацию собственных и публичных
        привычек."""

        # GET-запрос на получение всех привычек
        response = self.client.get(
            self.get_detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на пользователя объекта Habit
        self.assertEqual(
            response.json().get('habit_user'),
            self.user_test.email
        )

    def test_user_can_get_detail_habit_correctly_public(self):
        """Авторизованный пользователь может просматривать детализированную информацию собственных и публичных
        привычек."""

        # Получение маршрута для публичного объекта Habit для второго пользователя
        self.get_detail_user_2_public_url = f'/habits/{self.habit_object_2_public.pk}/'

        # GET-запрос на получение всех привычек
        response = self.client.get(
            self.get_detail_user_2_public_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка, что пользователь объекта Habit второго пользователя не есть тестовый пользователь
        self.assertTrue(
            response.json().get('habit_user') != self.user_test.email
        )

        # Проверка публичности привычки
        self.assertTrue(
            response.json().get('is_published')
        )

    def test_user_cannot_get_detail_not_owner_non_public_habit(self):
        """Авторизованный пользователь не может просматривать детализированную информацию чужих и непубличных
        привычек."""

        # Получение маршрута для непубличного объекта Habit для второго пользователя
        self.get_detail_user_2_non_public_url = f'/habits/{self.habit_object_2.pk}/'

        # GET-запрос на получение всех привычек
        response = self.client.get(
            self.get_detail_user_2_non_public_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка, что пользователь объекта Habit второго пользователя не есть тестовый пользователь
        self.assertTrue(
            response.json().get('habit_user') != self.user_test.email
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

        # Проверка публичности привычки
        self.assertFalse(
            response.json().get('is_published')
        )


class HabitUpdateTestCase(HabitModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.get_habits_url = '/habits/'
        # маршрут до непубличного объекта Habit тестового пользователя
        self.get_update_url = f'/habits/update/{self.habit_object_1.pk}/'

        self.update_date = {
            'habit_user': self.user_test.email,
            'place': 'Улица',
            'date_time': '2023-09-24T19:00:00Z',
            'action': 'Делать зарядку',
            'interval': 'Ежедневно',
            'execution_time': '120',
            'reward': 'Съесть шоколадку',
            'is_published': False,
        }

    def test_user_can_update_habits_correctly(self):
        """Авторизованный пользователь может изменить только собственные привычки."""

        # Получение текущего места для последующего изменения
        self.assertTrue(
            self.habit_object_1.place == 'Дом'
        )

        # PATCH-запрос на изменение непубличной привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            self.update_date,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка на собственника привычки
        self.assertEqual(
            response.json().get('habit_user'),
            self.user_test.email
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Получение содержимого ответа для измененного поля <place>
        self.assertTrue(
            response.json().get('place') == 'Улица'
        )

    def test_user_cannot_update_habits_without_authentication(self):
        """Неавторизованные пользователи не могут изменять объекты модели Habit."""

        # PATCH-запрос на изменение непубличной привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            self.update_date,
            headers=None,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_update_not_owner_habit(self):
        """Авторизованный пользователь не может изменить информацию чужих привычек."""

        # маршрут до непубличной привычки второго пользователя
        self.get_update_user_2_non_public_url = f'/habits/update/{self.habit_object_2.pk}/'

        # Проверка публичности привычки
        self.assertFalse(
            self.habit_object_2.is_published
        )

        # PATCH-запрос на изменение непубличной привычки второго пользователя от тестового пользователя
        response = self.client.patch(
            self.get_update_user_2_non_public_url,
            self.update_date,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_update_not_owner_public_habit(self):
        """Авторизованный пользователь не может изменить информацию чужих публичных привычек."""

        # маршрут до публичной привычки второго пользователя
        self.get_update_user_2_public_url = f'/habits/update/{self.habit_object_2_public.pk}/'

        # Проверка публичности привычки
        self.assertTrue(
            self.habit_object_2_public.is_published
        )

        # PATCH-запрос на изменение непубличной привычки второго пользователя от тестового пользователя
        response = self.client.patch(
            self.get_update_user_2_public_url,
            self.update_date,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_update_habit_without_reward_and_pleasant_habit(self):
        """При обновлении собственной привычки авторизованный пользователь должен указать либо <reward>, либо
        <pleasant_habit>."""

        # PATCH-запрос на изменение привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            {
                'habit_user': self.user_test.email,
                'place': 'Улица',
                'date_time': '2023-09-24T19:00:00Z',
                'action': 'Делать зарядку',
                'interval': 'Ежедневно',
                'execution_time': '120'
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'reward_or_pleasant_habit_fields': ["Необходимо указать ЛИБО 'reward', ЛИБО 'pleasant_habit'."]}
        )

    def test_user_cannot_update_habit_with_time_more_than_1_per_hour(self):
        """При обновлении собственной привычки авторизованный пользователь не может изменить время так, чтобы 1 привычка
        была чаще, чем 1 в час."""

        # PATCH-запрос на изменение привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            {
                'habit_user': self.user_test.email,
                'place': 'Улица',
                'date_time': '2023-09-24T20:00:00Z',
                'action': 'Делать зарядку',
                'interval': 'Ежедневно',
                'execution_time': '120',
                'reward': 'Ты крут!',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'date_time': ['Для одного пользователя необходимо устанавливать привычку не чаще 1 в час.']}
        )

    def test_user_cannot_create_habit_with_execution_time_less_then_or_equal_0(self):
        """Авторизованный пользователь может изменять свои привычки, поля <execution_time> которых должны быть
        в интервале от 0 до 120 секунд."""

        # PATCH-запрос на изменение привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            {
                'habit_user': self.user_test.email,
                'place': 'Улица',
                'date_time': '2023-09-24T10:00:00Z',
                'action': 'Делать зарядку',
                'interval': 'Ежедневно',
                'execution_time': '0',
                'reward': 'Ты крут!',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )

    def test_user_cannot_create_habit_with_execution_time_less_then_or_equal_120(self):
        """Авторизованный пользователь может изменять свои привычки, поля <execution_time> которых должны быть
        в интервале от 0 до 120 секунд."""

        # PATCH-запрос на изменение привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            {
                'habit_user': self.user_test.email,
                'place': 'Улица',
                'date_time': '2023-09-24T10:00:00Z',
                'action': 'Делать зарядку',
                'interval': 'Ежедневно',
                'execution_time': '150',
                'reward': 'Ты крут!',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )


class HabitDeleteTestCase(HabitModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.get_habits_url = '/habits/'
        # маршрут до непубличного объекта Habit тестового пользователя
        self.get_delete_url = f'/habits/delete/{self.habit_object_1.pk}/'

    def test_user_cannot_delete_habit_without_authentication(self):
        """Неавторизованные пользователи не могут удалять свои привычки."""

        # DELETE-запрос на удаление привычки
        response = self.client.delete(
            self.get_delete_url,
            headers=None,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_delete_not_owner_habit_non_public(self):
        """Авторизованные пользователи не могут удалять чужие непубличные привычки."""

        # DELETE-запрос на удаление чужой непубличной привычки
        response = self.client.delete(
            self.get_delete_url,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка на публичность привычки
        self.assertFalse(
            self.habit_object_1.is_published
        )

        # Проверка на собственника привычки
        self.assertTrue(
            self.habit_object_1.habit_user != self.user_2.email
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_delete_not_owner_habit_public(self):
        """Авторизованные пользователи не могут удалять чужие непубличные привычки."""

        # маршрут до публичного объекта Habit тестового пользователя
        self.get_delete_public_url = f'/habits/delete/{self.habit_object_1_public.pk}/'

        # DELETE-запрос на удаление чужой непубличной привычки
        response = self.client.delete(
            self.get_delete_public_url,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка на публичность привычки
        self.assertTrue(
            self.habit_object_1_public.is_published
        )

        # Проверка на собственника привычки
        self.assertTrue(
            self.habit_object_1_public.habit_user != self.user_2.email
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )


class PleasantHabitCreateTestCase(HabitModelTestCase):
    def setUp(self) -> None:
        super().setUp()
        # Получение маршрутов
        self.create_url = '/habits/pleasant/create/'

        # Сырые данные для создания PleasantHabit
        self.raw_pleasant_habit_data = {
            'habit_user': self.user_test.email,
            'place': 'Работа',
            'action': 'Делать разминку'
        }

    def test_user_cannot_create_pleasant_habit_without_authentication(self):
        """Пользователь не может создавать объекты без авторизации."""

        # Количество приятных привычек до создания
        self.assertTrue(
            PleasantHabit.objects.count() == 3
        )

        # POST-запрос на создание приятной привычки
        response = self.client.post(
            self.create_url,
            self.raw_pleasant_habit_data,
            headers=None,
            format='json'
        )

        # Количество привычек после создания
        self.assertTrue(
            PleasantHabit.objects.count() == 3
        )

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_create_pleasant_habit_with_execution_time_more_then_120(self):
        """Пользователь может создавать объекты модели PleasantHabit с полем <execution_time>, интервал которого
        должен быть в диапазоне от 0 до 120 секунд."""

        # Дополнение сырых данных недостающими полями
        self.raw_pleasant_habit_data['date_time'] = '2023-09-24T21:00:00Z'
        self.raw_pleasant_habit_data['execution_time'] = '130'

        # POST-запрос на создание приятной привычки
        response = self.client.post(
            self.create_url,
            self.raw_pleasant_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )

    def test_user_cannot_create_pleasant_habit_with_execution_time_less_then_or_equal_0(self):
        """Пользователь может создавать объекты модели PleasantHabit с полем <execution_time>, интервал которого должен
        быть в диапазоне от 0 до 120 секунд."""

        # Дополнение сырых данных недостающими полями
        self.raw_pleasant_habit_data['date_time'] = '2023-09-24T21:00:00Z'
        self.raw_pleasant_habit_data['execution_time'] = '0'

        # POST-запрос на создание приятной привычки
        response = self.client.post(
            self.create_url,
            self.raw_pleasant_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )

    def test_user_cannot_create_pleasant_habit_more_than_1_per_hour(self):
        """Пользователь может создавать объекты модели PleasantHabit не чаще, чем 1 в час."""
        # POST-запрос на создание приятной привычки
        response = self.client.post(
            self.create_url,
            {
                'habit_user': self.user_2.email,
                'place': 'Работа',
                'action': 'Делать разминку',
                'date_time': '2023-09-24T20:00:00Z',
                'execution_time': '120',
            },
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'date_time': ['Для одного пользователя необходимо устанавливать привычку не чаще 1 в час.']}
        )

    def test_user_can_create_pleasant_habit_correctly(self):
        """Пользователь может создавать объекты модели PleasantHabit корректно."""

        # Дополнение сырых данных недостающими полями
        self.raw_pleasant_habit_data['date_time'] = '2023-09-24T21:00:00Z'
        self.raw_pleasant_habit_data['execution_time'] = '120'

        # Количество приятных привычек до создания
        self.assertTrue(
            PleasantHabit.objects.count() == 3
        )

        # Отключение отложенной задачи
        self.patcher = patch('habits.tasks.register_habit.delay')
        self.mock_task = self.patcher.start()

        # POST-запрос на создание приятной привычки
        response = self.client.post(
            self.create_url,
            self.raw_pleasant_habit_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Включение отложенной задачи
        self.patcher.stop()

        # Количество привычек после создания
        self.assertTrue(
            PleasantHabit.objects.count() == 4
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


class PleasantHabitGetTestCase(HabitModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.get_habits_url = '/habits/pleasant/'
        # маршрут до публичного объекта PleasantHabit второго пользователя
        self.get_detail_url = f'/habits/pleasant/{self.pleasant_habit_user_2_published.pk}/'

    def test_user_can_get_pleasant_habits_correctly(self):
        """Авторизованный пользователь может просматривать только публичные и собственные приятные привычки."""

        # GET-запрос на получение всех приятных привычек второго пользователя
        response = self.client.get(
            self.get_habits_url,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка количества объектов в содержании ответа
        self.assertTrue(
            response.json().get('count') == 2
        )

        # Проверка количества объектов в базе данных
        self.assertTrue(
            PleasantHabit.objects.count() == 3
        )

    def test_user_cannot_get_pleasant_habits_without_authentication(self):
        """Неавторизованные пользователи не имеют доступа к объектам модели PleasantHabit."""

        # GET-запрос на получение всех приятных привычек
        response = self.client.get(
            self.get_habits_url,
            headers=None,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_can_get_detail_pleasant_habit_correctly_owner(self):
        """Авторизованный пользователь может просматривать детализированную информацию собственных и публичных
        приятных привычек."""

        # маршрут до непубличного объекта PleasantHabit второго пользователя
        self.get_detail_url_non_public = f'/habits/pleasant/{self.pleasant_habit_user_2_unpublished.pk}/'

        # GET-запрос на получение всех приятных привычек второго пользователя
        response = self.client.get(
            self.get_detail_url_non_public,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на пользователя объекта PleasantHabit
        self.assertEqual(
            response.json().get('habit_user'),
            self.user_2.email
        )

    def test_user_can_get_detail_pleasant_habit_correctly_public(self):
        """Авторизованный пользователь может просматривать детализированную информацию собственных и публичных
        привычек."""

        # GET-запрос на получение всех приятных привычек тестового пользователя
        response = self.client.get(
            self.get_detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка, что пользователь объекта PleasantHabit тестового пользователя не есть тестовый пользователь
        self.assertTrue(
            response.json().get('habit_user') != self.user_test.email
        )

        # Проверка публичности привычки
        self.assertTrue(
            response.json().get('is_published')
        )

    def test_user_cannot_get_detail_not_owner_non_public_pleasant_habit(self):
        """Авторизованный пользователь не может просматривать детализированную информацию чужих и непубличных,
        приятных привычек."""

        # Получение маршрута для непубличного объекта Habit для второго пользователя
        self.get_detail_user_2_non_public_url = f'/habits/pleasant/{self.pleasant_habit_user_2_unpublished.pk}/'

        # GET-запрос на получение всех привычек
        response = self.client.get(
            self.get_detail_user_2_non_public_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка, что пользователь объекта Habit второго пользователя не есть тестовый пользователь
        self.assertTrue(
            response.json().get('habit_user') != self.user_2.email
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

        # Проверка публичности привычки
        self.assertFalse(
            response.json().get('is_published')
        )


class PleasantHabitUpdateTestCase(HabitModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # маршрут до непубличного объекта PleasantHabit тестового пользователя
        self.get_update_url = f'/habits/pleasant/update/{self.pleasant_habit_test.pk}/'

        # Данные для обновления
        self.update_date = {
            'habit_user': self.user_test.email,
            'place': 'Улица',
            'date_time': '2023-09-24T19:00:00Z',
            'action': 'Делать зарядку',
            'execution_time': '120',
            'is_published': False,
        }

    def test_user_can_update_pleasant_habits_correctly(self):
        """Авторизованный пользователь может изменить только собственные привычки."""

        # Получение текущего места для последующего изменения
        self.assertTrue(
            self.habit_object_1.place == 'Дом'
        )

        # PATCH-запрос на изменение непубличной приятной привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            self.update_date,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка на собственника приятной привычки
        self.assertEqual(
            response.json().get('habit_user'),
            self.user_test.email
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Получение содержимого ответа для измененного поля <place>
        self.assertTrue(
            response.json().get('place') == 'Улица'
        )

    def test_user_cannot_update_pleasant_habits_without_authentication(self):
        """Неавторизованные пользователи не могут изменять объекты модели PleasantHabit."""

        # PATCH-запрос на изменение непубличной приятной привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            self.update_date,
            headers=None,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_update_not_owner_pleasant_habit(self):
        """Авторизованный пользователь не может изменить информацию чужих привычек."""

        # маршрут до непубличной приятной привычки второго пользователя
        self.get_update_user_2_non_public_url = f'/habits/pleasant/update/{self.pleasant_habit_user_2_unpublished.pk}/'

        # Проверка публичности привычки
        self.assertFalse(
            self.pleasant_habit_user_2_unpublished.is_published
        )

        # PATCH-запрос на изменение непубличной приятной привычки второго пользователя от тестового пользователя
        response = self.client.patch(
            self.get_update_user_2_non_public_url,
            self.update_date,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_update_not_owner_public_pleasant_habit(self):
        """Авторизованный пользователь не может изменить информацию чужих публичных привычек."""

        # маршрут до публичной приятной привычки второго пользователя
        self.get_update_user_2_public_url = f'/habits/pleasant/update/{self.pleasant_habit_user_2_published.pk}/'

        # Проверка публичности привычки
        self.assertTrue(
            self.pleasant_habit_user_2_published.is_published
        )

        # PATCH-запрос на изменение непубличной приятной привычки второго пользователя от тестового пользователя
        response = self.client.patch(
            self.get_update_user_2_public_url,
            self.update_date,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_update_pleasant_habit_with_time_more_than_1_per_hour(self):
        """При обновлении собственной приятной привычки авторизованный пользователь не может изменить время так, чтобы
        1 приятный привычка была чаще, чем 1 в час."""

        # маршрут до непубличного объекта PleasantHabit второго пользователя
        self.get_update_url = f'/habits/pleasant/update/{self.pleasant_habit_user_2_unpublished.pk}/'

        # PATCH-запрос на изменение приятной привычки второго пользователя
        response = self.client.patch(
            self.get_update_url,
            {
                'habit_user': self.user_2.email,
                'place': 'Улица',
                'date_time': '2023-09-24T20:00:00Z',
                'action': 'Делать зарядку',
                'execution_time': '120',
            },
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'date_time': ['Для одного пользователя необходимо устанавливать привычку не чаще 1 в час.']}
        )

    def test_user_cannot_create_pleasant_habit_with_execution_time_less_then_or_equal_0(self):
        """Авторизованный пользователь может изменять свои приятные привычки, поля <execution_time> которых должны быть
        в интервале от 0 до 120 секунд."""

        # PATCH-запрос на изменение привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            {
                'habit_user': self.user_test.email,
                'place': 'Улица',
                'date_time': '2023-09-24T10:00:00Z',
                'action': 'Делать зарядку',
                'execution_time': '0',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )

    def test_user_cannot_create_pleasant_habit_with_execution_time_less_then_or_equal_120(self):
        """Авторизованный пользователь может изменять свои приятные привычки, поля <execution_time> которых должны быть
        в интервале от 0 до 120 секунд."""

        # PATCH-запрос на изменение приятной привычки тестового пользователя
        response = self.client.patch(
            self.get_update_url,
            {
                'habit_user': self.user_test.email,
                'place': 'Улица',
                'date_time': '2023-09-24T10:00:00Z',
                'action': 'Делать зарядку',
                'execution_time': '150',
            },
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'execution_time': {'invalid_time': 'Максимальное время выполнения — 120 сек.'}}
        )


class PleasantHabitDeleteTestCase(HabitModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # маршрут до непубличного объекта PleasantHabit тестового пользователя
        self.get_delete_url = f'/habits/pleasant/delete/{self.pleasant_habit_test.pk}/'

    def test_user_cannot_delete_pleasant_habit_without_authentication(self):
        """Неавторизованные пользователи не могут удалять свои привычки."""

        # DELETE-запрос на удаление приятной привычки
        response = self.client.delete(
            self.get_delete_url,
            headers=None,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_delete_not_owner_pleasant_habit_non_public(self):
        """Авторизованные пользователи не могут удалять чужие непубличные привычки."""

        # DELETE-запрос на удаление чужой, непубличной, приятной привычки
        response = self.client.delete(
            self.get_delete_url,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка на публичность привычки
        self.assertFalse(
            self.pleasant_habit_test.is_published
        )

        # Проверка на собственника привычки
        self.assertTrue(
            self.pleasant_habit_test.habit_user != self.user_2.email
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_delete_not_owner_habit_public(self):
        """Авторизованные пользователи не могут удалять чужие непубличные привычки."""

        # маршрут до публичного объекта PleasantHabit второго пользователя
        self.get_delete_public_url = f'/habits/pleasant/delete/{self.pleasant_habit_user_2_published.pk}/'

        # DELETE-запрос на удаление чужой непубличной привычки
        response = self.client.delete(
            self.get_delete_public_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка на публичность привычки
        self.assertTrue(
            self.pleasant_habit_user_2_published.is_published
        )

        # Проверка на собственника привычки
        self.assertTrue(
            self.pleasant_habit_user_2_published.habit_user != self.user_2.email
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )
