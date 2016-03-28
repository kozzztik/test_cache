app.controller("GetMoneyCtrl", ['$scope', 'Restangular', '$q', '$location',
function ($scope, Restangular, $q, $location) {
    if (!user_card_number) {
        $location.path('/');
        return
    }
    if (!get_money_count) {
        $location.path('/');
        return
    }
    $scope.card_number = user_card_number.replace(/(\d{4})(\d{4})(\d{4})(\d{0,4})/g, "$1-$2-$3-$4");
    $scope.got_money = get_money_count;
    get_money_count = null;
    Restangular.one('get_money').customPOST({value: $scope.got_money * 100}).then(function(resp){
        if (resp.success) {
            $scope.balance = resp.result / 100;
            $scope.date_time = resp.time;
            $scope.loaded = true;
        } else {
            error_text = resp.reason;
            error_back_url = '/actions';
            $location.path('/error');
        }
    }, function(resp){
        error_text = resp;
        $location.path('/error');
        error_back_url = '/';
    }
    );
}]);