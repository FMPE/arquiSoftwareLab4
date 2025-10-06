"""
Script de debugging para verificar que los endpoints de auth funcionan
"""
import asyncio
import aiohttp
import json

async def test_auth_endpoints():
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Auth Endpoints Debug")
    print(f"Base URL: {base_url}")
    
    async with aiohttp.ClientSession() as session:
        # 1. Test health endpoint
        print("\n1. Testing health endpoint...")
        try:
            async with session.get(f"{base_url}/health") as response:
                print(f"   Health Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"   Health Data: {data}")
                else:
                    text = await response.text()
                    print(f"   Health Error: {text}")
        except Exception as e:
            print(f"   Health Exception: {e}")
        
        # 2. Test API docs
        print("\n2. Testing API docs...")
        try:
            async with session.get(f"{base_url}/docs") as response:
                print(f"   Docs Status: {response.status}")
        except Exception as e:
            print(f"   Docs Exception: {e}")
        
        # 3. Test register endpoint specifically
        print("\n3. Testing register endpoint...")
        user_data = {
            "username": "debug_user_001",
            "email": "debug001@test.com", 
            "password": "test123",
            "full_name": "Debug User"
        }
        
        try:
            async with session.post(
                f"{base_url}/api/v1/auth/register",
                json=user_data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                print(f"   Register Status: {response.status}")
                print(f"   Register Headers: {dict(response.headers)}")
                
                if response.status == 201:
                    data = await response.json()
                    print(f"   Register Success: {data}")
                else:
                    text = await response.text()
                    print(f"   Register Error Body: {text}")
                    
        except Exception as e:
            print(f"   Register Exception: {e}")
            import traceback
            traceback.print_exc()
        
        # 4. Test with another user
        print("\n4. Testing register with different user...")
        user_data2 = {
            "username": "debug_user_002",
            "email": "debug002@test.com",
            "password": "test123", 
            "full_name": "Debug User 2"
        }
        
        try:
            async with session.post(
                f"{base_url}/api/v1/auth/register",
                json=user_data2
            ) as response:
                print(f"   Register2 Status: {response.status}")
                if response.status != 201:
                    text = await response.text()
                    print(f"   Register2 Error: {text}")
                    
        except Exception as e:
            print(f"   Register2 Exception: {e}")
        
        # 5. Test login endpoint
        print("\n5. Testing login endpoint...")
        try:
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            
            async with session.post(
                f"{base_url}/api/v1/auth/login",
                data=login_data  # OAuth2PasswordRequestForm uses form data
            ) as response:
                print(f"   Login Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"   Login Success: Got token")
                else:
                    text = await response.text()
                    print(f"   Login Error: {text}")
                    
        except Exception as e:
            print(f"   Login Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_auth_endpoints())
