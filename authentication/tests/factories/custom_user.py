import factory
from django.contrib.auth import get_user_model


class CustomUserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: "user_{}@example.com".format(n))
    username = factory.Faker("first_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = "password"

    class Meta:
        model = get_user_model()