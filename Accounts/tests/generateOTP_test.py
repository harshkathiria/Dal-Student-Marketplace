from accounts.generateOTP import generate_otp

OTP_LOWER_LIMIT = 100000
OTP_UPPER_LIMIT = 999999


# def test_generate_otp():
#     otp = generate_otp()
#     assert isinstance(otp, str)
#     assert len(otp) == 6
#     assert otp.isdigit()
#
#
# def test_generate_otp_multiple_times():
#     otps = set()
#     for i in range(100):
#         otp = generate_otp()
#         otps.add(otp)
#     assert len(otps) == 100
#
#
# def test_generate_otp_using_same_seed():
#     random.seed(123)
#     otp1 = generate_otp()
#     otp2 = generate_otp()
#     assert otp1 != otp2
#
#
# def test_generate_otp_coverage():
#     # this test checks the coverage of the generate_otp function
#     with pytest.raises(TypeError):
#         generate_otp(5)

def test_generate_otp():
    # Test if generated OTP is within the allowed limit
    for i in range(100):
        otp = generate_otp()
        assert otp >= OTP_LOWER_LIMIT
        assert otp <= OTP_UPPER_LIMIT

    # Test if the generated OTPs are unique
    otp_list = []
    for i in range(100):
        otp = generate_otp()
        assert otp not in otp_list
        otp_list.append(otp)
