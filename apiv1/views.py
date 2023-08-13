from .imports import *


class RateThrottel(ScopedRateThrottle):
    THROTTLE_RATES = {
        'create_rate': '1/second',
    }


class CreateEventAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            factory = RepositoryFactory()
            event_repo: IEventRepository = factory.create_event_repository()
            user_repo: IUserRepository = factory.create_user_repository()

            usecase = CreateEvent(event_repo, user_repo)
            data = request.data

            serializer = RequestEventSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            
            event = Event(
                id=EventId(uuid.uuid4()).id,
                name=EventName(validated_data['name']).name,
                is_confirmed=IsConfirmed(False).is_confirmed,
                created_at=datetime.datetime.now().isoformat()
            )

            result = usecase.create_event(
                event,
                user_ids=list(validated_data['user_ids'])
            )

            if type(result) is str:
                message = json.dumps({"message": result}, ensure_ascii=False)
                return Response(message, status.HTTP_400_BAD_REQUEST)

            serializer = EventSerializer(result)

            return Response(serializer.data, status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)
        

class ConfirmEventAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            factory = RepositoryFactory()
            event_repo: IEventRepository = factory.create_event_repository()

            usecase = ConfirmEvent(event_repo)

            event_id = self.kwargs.get('event_id')

            result = usecase.confirm_event(event_id)

            if result is not None:
                message = json.dumps({"message": result}, ensure_ascii=False)
                return Response(message, status.HTTP_400_BAD_REQUEST)

            serializer = EventSerializer(result)

            return Response(serializer.data, status.status.HTTP_200_OK)

        except ValueError as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)


class AddUsersEventAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            factory = RepositoryFactory()
            event_repo: IEventRepository = factory.create_event_repository()

            usecase = AddUsersEvent(event_repo)
            data = request.data

            serializer = AddUsersEventSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            result = usecase.add_users_event(
                validated_data['event_id'],
                user_ids=list(validated_data['user_ids'])
            )

            if result is None:
                return Response({"message": "不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)

            return Response({"event_id":validated_data['event_id'], "user_ids": result}, status.HTTP_200_OK)

        except ValueError as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)


class CreatePayAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            factory = RepositoryFactory()
            pay_repo: IPayRepository = factory.create_pay_repository()

            usecase = CreatePay(pay_repo)
            data = request.data

            serializer = RequestPaySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            pay = Pay(
                id=uuid.uuid4(),
                name=PayName(validated_data['name']).name,
                event_id=EventId(validated_data['event_id']).id,
                user_id=UserId(validated_data['user_id']).id,
                amount_pay=AmountPay(
                    int(validated_data['amount_pay'])).amount_pay,
                related_users=list(validated_data['related_users']),
                created_at=datetime.datetime.now().isoformat()
            )

            result = usecase.create_pay(pay)

            if result == None:
                return Response({"message": "不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)

            serializer = PaySerializer(result)

            return Response(serializer.data, status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)


class GetEventsAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
            return Response({"message": "イベントの読み込みに失敗しました"}, status.HTTP_400_BAD_REQUEST)
        
class GetEventAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        event_repo: IEventRepository = factory.create_event_repository()

        usecase = GetEvent(event_repo)
        event_id = self.kwargs.get('event_id')

        try:
            result = EventSerializer(usecase.get_event(event_id)).data

            if not result:
                return Response(result, status.HTTP_204_NO_CONTENT)

            return Response(result, status.HTTP_200_OK)
        except:
            return Response({"message": "イベントの読み込みに失敗しました"}, status.HTTP_400_BAD_REQUEST)


class GetPaysAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        pay_repo: IPayRepository = factory.create_pay_repository()
        user_repo: IUserRepository = factory.create_user_repository()

        get_pay_usecase = GetPays(pay_repo)
        user_ids_mapping_usecase = GetUsersDictByEventId(user_repo)

        event_id = self.kwargs.get('event_id')

        try:
            event_id = EventId(event_id).id
            results = get_pay_usecase.get_pays(event_id)

            if not results:
                return Response(results, status.HTTP_204_NO_CONTENT)

            # eventの中のuserを全て取り出し、{user_id:name}にマッピング
            user_ids_name = user_ids_mapping_usecase.get_users_dict_by_event_id(
                results[0].event_id)

            if not user_ids_name:
                return Response({"message": "支払いがないか、不正なパラメータ"}, status.HTTP_400_BAD_REQUEST)

            result = [{
                "id": i.id,
                "name": i.name,
                "event_id": i.event_id,
                "user": {
                    "user_id": i.user_id,
                    "user_name": user_ids_name[str(i.user_id)]
                },
                "amount_pay": i.amount_pay,
                "related_users": [{"user_id": str(user_id), "user_name": user_ids_name[str(user_id)]} for user_id in i.related_users],
                "created_at": i.created_at
            }
                for i in results]

            return Response(result, status.HTTP_200_OK)

        except:
            return Response({"message": "invalid access"}, status.HTTP_400_BAD_REQUEST)


class ReadQrAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)

        usecase = ReadQr()
        qr = Qr(
            id=uuid.uuid4(),
            binary_data=data['binary_data']
        )
        result = usecase.read_qr(qr)

        if result is None:
            return Response({"message": "QRの読み込みに失敗しました"}, status.HTTP_400_BAD_REQUEST)

        return Response({"qr_content": result}, status.HTTP_200_OK)


class AdjustEventAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        user_repo: IUserRepository = factory.create_user_repository()

        usecase = AdjustmentEvent()
        user_ids_mapping_usecase = GetUsersDictByEventId(user_repo)

        event_id = self.kwargs.get('event_id')

        results = usecase.adjust_event(event_id)

        if results == None:
            return Response({"message": "支払いがないか、不正なパラメータ"}, status.HTTP_400_BAD_REQUEST)

        # eventの中のuserを全て取り出し、{user_id:name}にマッピング
        user_ids_name = user_ids_mapping_usecase.get_users_dict_by_event_id(
            event_id)

        if not user_ids_name:
            return Response({"message": "支払いがないか、不正なパラメータ"}, status.HTTP_400_BAD_REQUEST)

        result = [{
            "id": i.id,
            "event_id": i.event_id,
            "adjust_user": {"adjust_user_id": i.adjust_user_id, "adjust_user_name": user_ids_name[str(i.adjust_user_id)]},
            "adjusted_user": {"adjusted_user_id": i.adjusted_user_id, "adjusted_user_name": user_ids_name[str(i.adjusted_user_id)]},
            "amount_pay": i.amount_pay,
            "created_at": i.created_at
        } for i in results]

        if not result:
            return Response({"message": "計算に失敗しました"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(result, status.HTTP_200_OK)


class RequestFriendAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            factory = RepositoryFactory()
            friend_repo: IFriendRepository = factory.create_friend_repository()

            usecase = RequestFriend(friend_repo)
            data = request.data

            serializer = RequestFriendSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            approval = Approval(False)
            friend = Friend(
                id=FriendId(uuid.uuid4()).id,
                request_user_id=UserId(validated_data['request_user_id']).id,
                requested_user_id=UserId(
                    validated_data['requested_user_id']).id,
                approval=approval,
                created_at=datetime.datetime.now().isoformat()
            )

            result = usecase.request_friend(friend)

            if result == None:
                return Response({"message": "不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)

            if type(result) is str:
                return Response({"message": result}, status.HTTP_400_BAD_REQUEST)

            result = vars(result)

            return Response(result, status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)


class ApproveFriendAPIView(views.APIView):
    throttle_classes = [RateThrottel]
    throttle_scope = 'create_rate'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
            id=uuid.uuid4(),
            request_user_id=UserId(validated_data['request_user_id']).id,
            requested_user_id=UserId(validated_data['requested_user_id']).id,
            approval=approval,
            created_at=datetime.datetime.now().isoformat()
        )

        result = usecase.request_friend(friend)

        if result == None:
            return Response({"message": "不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)

        if type(result) is str:
            return Response({"message": result}, status.HTTP_400_BAD_REQUEST)

        result = vars(result)

        return Response(result, status.HTTP_201_CREATED)


class GetFriendsAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = []
        factory = RepositoryFactory()
        friend_repo: IFriendRepository = factory.create_friend_repository()

        user_id = self.kwargs.get('user_id')
        usecase = GetFriends(friend_repo)

        results = usecase.get_friend(user_id)

        if results == None:
            return Response({"message": "不正なリクエストです"}, status.HTTP_400_BAD_REQUEST)

        if type(results) is str:
            return Response({"message": results}, status.HTTP_400_BAD_REQUEST)

        if not results:
            return Response(results, status.HTTP_204_NO_CONTENT)
        
        for friend in results:
            #user_idじゃない方がfriendのuser_id
            if str(friend.requested_user_id) == user_id:
                result.append({
                "friend_user": {
                    "friend_user_id": friend.request_user_id,
                    "friend_user_name": friend.request_user_name,
                },
                "created_at": friend.created_at
                })
            elif str(friend.request_user_id) == user_id:
                result.append({
                "friend_user": {
                    "friend_user_id": friend.requested_user_id,
                    "friend_user_name": friend.requested_user_name,
                },
                "created_at": friend.created_at
                })

        return Response(result, status.HTTP_200_OK)


class ConvertUserIdNameAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        usecase = ConvertUserIdName()

        try:
            user_id = UserId(self.kwargs.get('user_id')).id
            result = usecase.convert_user_id_name(user_id)

            if result == None:
                return Response({"message": "ユーザが見つかりません"}, status.HTTP_400_BAD_REQUEST)

            return Response({"user_id": result}, status.HTTP_200_OK)

        except ValueError as e:
            return Response({"message": e}, status.HTTP_400_BAD_REQUEST)


class GetUsersDictByEventIdAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        factory = RepositoryFactory()
        user_repo: IUserRepository = factory.create_user_repository()
        usecase = GetUsersDictByEventId(user_repo)

        try:
            event_id = EventId(self.kwargs.get('event_id')).id
            result = usecase.get_users_dict_by_event_id(event_id)

            if result == None:
                return Response({"message": "ユーザが見つかりません"}, status.HTTP_400_BAD_REQUEST)

            return Response(result, status.HTTP_200_OK)

        except ValueError as e:
            return Response({"message": e}, status.HTTP_400_BAD_REQUEST)