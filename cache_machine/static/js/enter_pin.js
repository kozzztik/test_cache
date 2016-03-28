app.controller("EnterPinCtrl", ['$scope', 'Restangular', '$q', '$location',
function ($scope, Restangular, $q, $location) {
    if (!user_card_number) {
        $location.path('/');
    }
    $scope.input_label = 'Введите ПИН код';
    $scope.show_exit = true;
    $scope.enter_value = '';
    $scope.valid_number = false;
    $scope.press_key = function(num){
        $scope.error_text = '';
        if ($scope.enter_value.length < 4) {
            $scope.enter_value = $scope.enter_value + num;
            $scope.valid_number = $scope.enter_value.length == 4;
            $scope.show_value = $scope.enter_value.replace( /[0-9]/g, '*');
        }
    }
    $scope.send_card_number = function(){
        if ($scope.enter_value.length == 4) {
            Restangular.all('card_auth').post(null, {card_number: user_card_number, pin: $scope.enter_value}).then(function(resp){
                if (resp.success) {
                    user_name = resp.user_name;
                    $location.path('/actions');
                } else {
                    if (resp.card_locked){
                        error_text = 'Карта заблокирована';
                        error_back_url = '/enter_pin';
                        $location.path('/error');
                    } else {
                        error_text = 'Неправильный PIN код';
                        error_back_url = '/enter_pin';
                        $location.path('/error');
                    }
                }
            }, function(response) {
                error_text = 'Неизвестная ошибка';
                error_back_url = '/enter_pin';
                $location.path('/error');
            })
        }
    }
    $scope.clear_card_number = function(){
        $scope.enter_value='';
        $scope.show_value='';
        $scope.valid_number = false;
    }
}])