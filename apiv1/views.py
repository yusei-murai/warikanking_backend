from .imports import *

class RateThrottel(ScopedRateThrottle):
    THROTTLE_RATES = {
        'create_rate': '1/second',
    }

class CreateEventAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
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
            return Response(json.dumps({"message":"イベントの読み込みに失敗しました"}), status.HTTP_400_BAD_REQUEST)
    
class GetPaysAPIView(views.APIView):
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
    #permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):
        usecase = AdjustmentEvent()
        event_id = self.kwargs.get('event_id')
        
        results = usecase.adjust_event(event_id)
        
        if results == None:
            return Response({"message":"支払いがありません"}, status.HTTP_400_BAD_REQUEST)
        
        result = [vars(i) for i in results]
        
        if not result:
            return Response({"message":"計算に失敗しました"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(result, status.HTTP_200_OK)
    
class CreateFriendAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    #permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        pay_repo: IFriendRepository = factory.create_friend_repository()

        usecase = CreateFriend(pay_repo)
        data = request.data

        serializer = RequestFriendSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        friend = Friend(
            id = uuid.uuid4(),
            user_1_id=validated_data['user_1_id'],
            user_2_id=validated_data['user_2_id'],
            created_at = datetime.datetime.now().isoformat()
        )

        result = usecase.create_friend(friend)
        
        if result == None:
            return Response({"message":"不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)

        serializer = PaySerializer(result)
        
        return Response(serializer.data, status.HTTP_201_CREATED)