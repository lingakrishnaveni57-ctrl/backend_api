@router.post("/signup", summary="Signup with email", description="Registers a new user and sends OTP to email.")
def signup(data: UserSignup, db: Session = Depends(get_db)):
    otp = str(random.randint(100000, 999999))

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        return {"error": "Email already registered"}

    user = User(
        username=data.username,   # <-- include username
        email=data.email,
        password=hash_password(data.password),
        otp=otp,
        is_verified=False
    )
    db.add(user)
    db.commit()
    send_otp_email(data.email, otp)
    return {"message": "OTP sent to your email"}

