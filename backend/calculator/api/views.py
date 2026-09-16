from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from calculator.services.evaluator import ExpressionError, evaluate


class CalculateView(APIView):
    """Evaluate a calculator expression supplied by the user interface."""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        expression = request.data.get("expression")
        if not isinstance(expression, str):
            return Response(
                {"detail": "The expression must be a string."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            return Response({"result": evaluate(expression)})
        except ExpressionError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
