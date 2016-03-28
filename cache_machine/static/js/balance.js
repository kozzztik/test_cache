app.controller("BalanceCtrl", ['$scope', 'Restangular', '$q', '$location',
function ($scope, Restangular, $q, $location) {
    if (!user_card_number) {
        $location.path('/');
    }
    $scope.card_number = user_card_number.replace(/(\d{4})(\d{4})(\d{4})(\d{0,4})/g, "$1-$2-$3-$4");
    Restangular.one('check_balance').customPOST().then(function(resp){
        $scope.balance = resp.result / 100;
        $scope.date_time = resp.date;
        $scope.loaded = true;
    }, function(resp){
        error_text = resp;
        $location = '/error'
        error_back_url = '/';
    }
    );
}]);