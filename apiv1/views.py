from .imports import *

class RateThrottel(ScopedRateThrottle):
    THROTTLE_RATES = {
        'create_rate': '1/second',
    }

class CreateEventAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        event_repo: IEventRepository = factory.create_event_repository()
        user_repo: IUserRepository = factory.create_user_repository()

        usecase = CreateEvent(event_repo, user_repo)
        data = request.data

        serializer = RequestEventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        event = Event(
            id=uuid.uuid4(),
            name=validated_data['name'],
            created_at = datetime.datetime.now().isoformat()
        )

        result = usecase.create_event(
            event,
            user_ids=list(validated_data['user_ids'])
        )
        
        if type(result) is str:
            message = json.dumps({"message":result},ensure_ascii=False)
            return Response(message, status.HTTP_400_BAD_REQUEST)
            
        serializer = EventSerializer(result)
            
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class CreatePayAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        pay_repo: IPayRepository = factory.create_pay_repository()

        usecase = CreatePay(pay_repo)
        data = request.data

        serializer = RequestPaySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        pay = Pay(
            id = uuid.uuid4(),
            name=validated_data['name'],
            event_id=validated_data['event_id'],
            user_id=validated_data['user_id'],
            amount_pay=int(validated_data['amount_pay']),
            related_users=list(validated_data['related_users']),
            created_at = datetime.datetime.now().isoformat()
        )

        result = usecase.create_pay(pay)
        
        if result == None:
            return Response({"message":"不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)

        serializer = PaySerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class GetEventsAPIView(views.APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        event_repo: IEventRepository = factory.create_event_repository()

        usecase = GetEvents(event_repo)
        user_id = self.kwargs.get('user_id')
        
        try:
            user_id = uuid.UUID(user_id)
            results = usecase.get_events(user_id)
            
            result = [EventSerializer(i).data for i in results]
            
            if not result:
                return Response(result, status.HTTP_204_NO_CONTENT)
        
            return Response(result, status.HTTP_200_OK)
        except:
            return Response({"message":"イベントの読み込みに失敗しました"}, status.HTTP_400_BAD_REQUEST)
    
class GetPaysAPIView(views.APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        pay_repo: IPayRepository = factory.create_pay_repository()

        usecase = GetPays(pay_repo)
        event_id = self.kwargs.get('event_id')

        try:
            event_id = uuid.UUID(event_id)
            results = usecase.get_pays(event_id)
 
            result = [PaySerializer(i).data for i in results]
            
            if not result:
                return Response(result, status.HTTP_204_NO_CONTENT)
        
            return Response(result, status.HTTP_200_OK)
        
        except:
            return Response({"message":"invalid access"}, status.HTTP_400_BAD_REQUEST)
        
class ReadQrAPIView(views.APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)
        
        usecase = ReadQr()
        qr = Qr(
            id = uuid.uuid4(),
            binary_data = data['binary_data']
        )
        result = usecase.read_qr(qr)

        if result is None:
            return Response({"message":"QRの読み込みに失敗しました"}, status.HTTP_400_BAD_REQUEST)
        
        return Response({"qr_content":result}, status.HTTP_200_OK)
        
class AdjustEventAPIView(views.APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        usecase = AdjustmentEvent()
        event_id = self.kwargs.get('event_id')
        
        results = usecase.adjust_event(event_id)
        
        if results == None:
            return Response({"message":"支払いがないか、不正なパラメータ"}, status.HTTP_400_BAD_REQUEST)
        
        result = [vars(i) for i in results]
        
        if not result:
            return Response({"message":"計算に失敗しました"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(result, status.HTTP_200_OK)
    
class RequestFriendAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        friend_repo: IFriendRepository = factory.create_friend_repository()

        usecase = RequestFriend(friend_repo)
        data = request.data

        serializer = RequestFriendSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        approval = Approval(False)
        friend = Friend(
            id = uuid.uuid4(),
            request_user_id = validated_data['request_user_id'],
            requested_user_id = validated_data['requested_user_id'],
            approval = approval,
            created_at = datetime.datetime.now().isoformat()
        )

        result = usecase.request_friend(friend)
        
        if result == None:
            return Response({"message":"不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)
        
        if type(result) is str:
            return Response({"message":result}, status.HTTP_400_BAD_REQUEST)

        result = vars(result)
        
        return Response(result, status.HTTP_201_CREATED)
    
class ApproveFriendAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        friend_repo: IFriendRepository = factory.create_friend_repository()

        usecase = RequestFriend(friend_repo)
        data = request.data

        serializer = RequestFriendSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        approval = Approval(False)
        friend = Friend(
            id = uuid.uuid4(),
            request_user_id = validated_data['request_user_id'],
            requested_user_id = validated_data['requested_user_id'],
            approval = approval,
            created_at = datetime.datetime.now().isoformat()
        )

        result = usecase.request_friend(friend)
        
        if result == None:
            return Response({"message":"不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)
        
        if type(result) is str:
            return Response({"message":result}, status.HTTP_400_BAD_REQUEST)

        result = vars(result)
        
        return Response(result, status.HTTP_201_CREATED)
    
class ApproveFriendAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        friend_repo: IFriendRepository = factory.create_friend_repository()

        usecase = ApproveFriend(friend_repo)
        
        friend_id = self.kwargs.get('friend_id')

        result = usecase.approve_friend(friend_id)
        
        if result == None:
            return Response({"message":"不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)
        
        if type(result) is str:
            return Response({"message":result}, status.HTTP_400_BAD_REQUEST)

        result = vars(result)
        
        return Response(result, status.HTTP_201_CREATED)
    
class ConvertUserIdNameAPIView(views.APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        user_repo: IUserRepository = factory.create_user_repository()

        usecase = ConvertUserIdName(user_repo)

        try:
            user_id = UserId(self.kwargs.get('user_id')).id
            result = usecase.convert_user_id_name(user_id)
            
            if result == None:
                return Response({"message":"ユーザが見つかりません"}, status.HTTP_400_BAD_REQUEST)
        
            return Response({"user_id":result}, status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"message":e}, status.HTTP_400_BAD_REQUEST)