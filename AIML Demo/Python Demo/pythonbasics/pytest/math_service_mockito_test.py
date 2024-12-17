from mockito import when, verify, unstub
import math_service

def test_process_input():
    # Mock the `addnumbers` function as it exists in `math_service`
    when(math_service).addnumbers(30, 30).thenReturn(60)

    # Call the process_input function
    result = math_service.process_input(30, 30)
    
    print("Response from mock method:", result)

    # Assertions
    assert result == 60, f"Expected 60 but got {result}"

    # Verify that the mocked function was called
    verify(math_service).addnumbers(30, 30)

    # Cleanup the mock
    unstub()

# Run the test
if __name__ == "__main__":
    test_process_input()
    print("Test passed!")
