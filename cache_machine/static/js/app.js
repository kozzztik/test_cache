var app = angular.module('CacheMachineApp', [
    'ui.router',
    'restangular',
    'ngCookies'
])

app.config(function ($stateProvider, $urlRouterProvider, RestangularProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/templates/enter_data.html",
            controller: "EnterCardCtrl"
        })
        .state('error', {
            url: "/error",
            templateUrl: "/static/templates/error.html",
            controller: "ErrorCtrl"
        })
        .state('enter_pin', {
            url: "/enter_pin",
            templateUrl: "/static/templates/enter_data.html",
            controller: "EnterPinCtrl"
        })
        .state('actions', {
            url: "/actions",
            templateUrl: "/static/templates/actions.html",
            controller: function ($scope, Restangular, $q, $location) {
                if (!user_card_number) {
                    $location.path('/');
                }
                $scope.user_name=user_name;
            }
        })
        .state('logout', {
            url: "/logout",
            controller: "LogoutCtrl"
        })
        .state('balance', {
            url: "/balance",
            templateUrl: "/static/templates/balance.html",
            controller: "BalanceCtrl",
        })
        .state('get_money', {
            url: "/get_money",
            templateUrl: "/static/templates/enter_data.html",
            controller: "GetMoneyCtrl",
        })
        .state('get_money_result', {
            url: "/get_money_result",
            templateUrl: "/static/templates/get_money_result.html",
            controller: "GetMoneyCtrl",
        })

}).config(function($httpProvider, $cookiesProvider){
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }
);
var error_text = '';
var error_back_url = '';
var user_card_number = '';
var user_name = '';
var
app.controller("ErrorCtrl", ['$scope', 'Restangular', '$q',
function ($scope, Restangular, $q) {
    $scope.error_text=error_text;
    $scope.error_back_url=error_back_url;
}
]);

app.controller("LogoutCtrl", ['$scope', 'Restangular', '$q', '$location',
function ($scope, Restangular, $q, $location) {
    Restangular.all('card_auth').customGET().then(function(resp){
        user_card_number = '';
        user_name = '';
        $location.path('/');
    }, function(response) {
        user_card_number = '';
        user_name = '';
        $location.path('/');
    })

}
]);