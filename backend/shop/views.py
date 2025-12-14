from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .models import Sweet
from .serializers import RegisterSerializer, SweetSerializer


# ================= AUTH =================

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "is_staff": user.is_staff,  # <-- used by frontend
                    }
                )
            return Response({"error": "Invalid password"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


# ================= SWEETS =================

# 1️⃣ List sweets + Add sweet
class SweetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sweets = Sweet.objects.all()
        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        serializer = SweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# 2️⃣ Update & Delete Sweet
class SweetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        sweet = get_object_or_404(Sweet, pk=pk)
        serializer = SweetSerializer(sweet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        sweet = get_object_or_404(Sweet, pk=pk)
        sweet.delete()
        return Response({"message": "Sweet deleted successfully"})


# 3️⃣ Purchase Sweet (quantity based)
class PurchaseSweetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sweet = get_object_or_404(Sweet, pk=pk)

        qty = request.data.get("quantity")

        try:
            qty = int(qty)
        except ValueError:
            return Response({"error": "Quantity must be a number"}, status=400)

        if qty <= 0:
            return Response({"error": "Quantity must be greater than 0"}, status=400)

        if sweet.quantity < qty:
            return Response({"error": "Not enough stock"}, status=400)

        sweet.quantity -= qty
        sweet.save()

        return Response({
            "message": f"Purchased {qty} item(s)",
            "remaining_quantity": sweet.quantity
        })


# 4️⃣ Restock Sweet
class RestockSweetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        sweet = get_object_or_404(Sweet, pk=pk)

        # ✅ DEFAULT RESTOCK VALUE (CHANGE HERE)
        DEFAULT_RESTOCK_AMOUNT = 10   # change to 1 if you want

        amount = request.data.get("amount")

        # If amount not provided → use default
        if amount is None:
            amount = DEFAULT_RESTOCK_AMOUNT
        else:
            amount = int(amount)

        # Validation
        if amount <= 0:
            return Response(
                {"error": "Restock amount must be greater than 0"},
                status=400
            )

        sweet.quantity += amount
        sweet.save()

        return Response({
            "message": f"Sweet restocked by {amount}",
            "current_quantity": sweet.quantity
        })

# 5️⃣ Search & Filter
class SweetSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.GET.get("name")
        category = request.GET.get("category")

        sweets = Sweet.objects.all()

        if name:
            sweets = sweets.filter(name__icontains=name)
        if category:
            sweets = sweets.filter(category__icontains=category)

        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data)
