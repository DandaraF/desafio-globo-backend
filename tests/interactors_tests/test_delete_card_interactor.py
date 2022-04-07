from unittest.mock import MagicMock, patch

from _pytest.python_api import raises

from challenge_app.interactors.card.delete_card_interactor import (
    DeleteCardRequestModel, DeleteCardResponseModel, DeleteCardInteractor,
    CardNotExistsException)

patch_root = 'challenge_app.interactors.card.delete_card_interactor'


def test_delete_card_request_model():
    mock_json_data = {'card_id': "234d"}
    request = DeleteCardRequestModel(mock_json_data)

    assert request.card_id == '234d'


def test_delete_card_response_model():
    mock_deleted_id = MagicMock()
    response = DeleteCardResponseModel(mock_deleted_id)

    result = response()

    assert response.deleted_id == mock_deleted_id
    assert result == mock_deleted_id


@patch(f'{patch_root}.CardMongodbAdapter')
@patch(f'{patch_root}.DeleteCardRequestModel')
def test_delete_card_interactor(mock_request,
                                mock_adapter):
    interactor = DeleteCardInteractor(mock_adapter, mock_request)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


@patch(f'{patch_root}.CardMongodbAdapter')
@patch(f'{patch_root}.DeleteCardRequestModel')
def test_delete_card_interactor_check_if_card_exists(mock_request,
                                                     mock_adapter):
    interactor = DeleteCardInteractor(mock_adapter, mock_request)

    interactor.check_if_card_exists()

    mock_adapter.get_by_id.assert_called_with(interactor.request.card_id)


@patch(f'{patch_root}.CardMongodbAdapter')
def test_delete_card_interactor_check_if_card_exists_raises(
        mock_mongo_adapter):
    mock_request_model = MagicMock()
    mock_adapter = MagicMock()

    interactor = DeleteCardInteractor(mock_adapter, mock_request_model)

    interactor.adapter.get_by_id.return_value = None

    with raises(CardNotExistsException):
        interactor.check_if_card_exists()


@patch(f'{patch_root}.CardMongodbAdapter')
@patch(f'{patch_root}.DeleteCardRequestModel')
@patch(f'{patch_root}.DeleteCardResponseModel')
@patch.object(DeleteCardInteractor, 'check_if_card_exists')
def test_delete_card_interactor_run(mock_check_if_exists,
                                    mock_response,
                                    mock_request,
                                    mock_adapter):
    mock_delete = MagicMock()

    interactor = DeleteCardInteractor(mock_adapter, mock_request)

    result = interactor.run()

    mock_check_if_exists.assert_called_once_with()

    mock_adapter.delete.assert_called_once_with(mock_request.card_id)

    mock_response.assert_called_once_with(mock_adapter.delete(mock_delete))

    assert result == mock_response()


@patch(f'{patch_root}.CardMongodbAdapter')
@patch(f'{patch_root}.DeleteCardRequestModel')
@patch.object(DeleteCardInteractor, 'check_if_card_exists',
              side_effect=ValueError('Eita'))
def test_delete_card_interactor_run_raises(mock_check,
                                           mock_adapter,
                                           mock_request):

    interactor = DeleteCardInteractor(mock_adapter, mock_request)




