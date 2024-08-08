import requests
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from core.settings import ETHER_SCAN_API_KEY

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email",
                  "password", "password2", "ethereum_address","ethereum_balance")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }
    
    def get_eth_balance(self,user):
        print( user)
        if user.ethereum_address:
                
            url = 'https://api.etherscan.io/api'
            params = {
                'module': 'account',
                'action': 'balance',
                'address': user.ethereum_address,
                'tag': 'latest',
                'apikey': ETHER_SCAN_API_KEY

            }
            response = requests.get(url, params=params)
            
            data = response.json()
            print(data)
            if data['status'] == '1':
                balance = int(data['result']) / 10**18  # Convert Wei to Ether
                return balance
         
        return False
     
    
    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            ethereum_address=self.validated_data["ethereum_address"]
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        eth_balance=self.get_eth_balance(user)
        if eth_balance:
            print(eth_balance)
            user.ethereum_balance = float(eth_balance)
            
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff",
                  "ethereum_address", "first_name", "last_name","ethereum_balance")
