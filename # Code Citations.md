# Code Citations

## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name:
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      require
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email:
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email: {
      type: String,
      require
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      trim:
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      trim: true,
      lowercase: true,
    
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      trim: true,
      lowercase: true,
    },
    password: {
      type:
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      trim: true,
      lowercase: true,
    },
    password: {
      type: String,
      required: [true, 
```


## License: unknown
https://github.com/thefinethread/Support-Desk/blob/45e48b0c4b623646f198f0e55effbb919ef2f817/backend/models/User.js

```
(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      trim: true,
      lowercase: true,
    },
    password: {
      type: String,
      required: [true, 'Password is required']
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email,
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email:
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email:
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email:
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email:
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status
```


## License: unknown
https://github.com/EmerBV/NftHouse-Back-End-Advance/blob/ededcdccda19d3f07d1e5fbfc8f3f7d316e6d3fb/server/controllers/userController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status(400)
```


## License: unknown
https://github.com/MadaraRU/menu-app-backend/blob/9ba794092222d682818a1065510ee20d75854822/src/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status(400)
```


## License: unknown
https://github.com/jakubgasienica/MERN-app/blob/9fea14682691ac28e19ca512744121413dbfc0a0/backend/controllers/userController.ts

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status(400)
```


## License: unknown
https://github.com/UmeshGolani/Slack-Clone-Backend/blob/c45a04299fa21eccc3c96ecc91594fafec6ae4f7/controllers/authController.js

```
const { name, email, password } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    if (user) {
      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id.toString()),
      });
    } else {
      res.status(400)
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await User.findById(req.user.
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await User.findById(req.user.id).select('-password');
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await User.findById(req.user.id).select('-password');

    if (!user) {
      
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await User.findById(req.user.id).select('-password');

    if (!user) {
      return res.status(404).json({ message
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await User.findById(req.user.id).select('-password');

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await User.findById(req.user.id).select('-password');

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    res.json(user);
  }
```


## License: unknown
https://github.com/johnlandonwood/MobileBartendingApp/blob/f9ae89e9f7ef9bb3ad6f1a62f54556d35dc384d3/backend/routes/users.js

```
const user = await User.findById(req.user.id).select('-password');

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    res.json(user);
  } catch (error
```


## License: unknown
https://github.com/Alqatrony/swar_al-raqiyat_API/blob/b66f5dcaca79a8418661e01aa05fc37f664adcf0/middleware/auth.js

```
//
```


## License: unknown
https://github.com/Alqatrony/swar_al-raqiyat_API/blob/b66f5dcaca79a8418661e01aa05fc37f664adcf0/middleware/auth.js

```
// Get token from header
    const token = req
```


## License: unknown
https://github.com/Alqatrony/swar_al-raqiyat_API/blob/b66f5dcaca79a8418661e01aa05fc37f664adcf0/middleware/auth.js

```
// Get token from header
    const token = req.header('x-auth-token');
```


## License: unknown
https://github.com/Alqatrony/swar_al-raqiyat_API/blob/b66f5dcaca79a8418661e01aa05fc37f664adcf0/middleware/auth.js

```
// Get token from header
    const token = req.header('x-auth-token');

    // Check if token exists
    if
```


## License: unknown
https://github.com/Alqatrony/swar_al-raqiyat_API/blob/b66f5dcaca79a8418661e01aa05fc37f664adcf0/middleware/auth.js

```
// Get token from header
    const token = req.header('x-auth-token');

    // Check if token exists
    if (!token) {
      return res.status
```


## License: unknown
https://github.com/Alqatrony/swar_al-raqiyat_API/blob/b66f5dcaca79a8418661e01aa05fc37f664adcf0/middleware/auth.js

```
// Get token from header
    const token = req.header('x-auth-token');

    // Check if token exists
    if (!token) {
      return res.status(401).json({ message: 'No
```


## License: unknown
https://github.com/Alqatrony/swar_al-raqiyat_API/blob/b66f5dcaca79a8418661e01aa05fc37f664adcf0/middleware/auth.js

```
// Get token from header
    const token = req.header('x-auth-token');

    // Check if token exists
    if (!token) {
      return res.status(401).json({ message: 'No token, authorization denied' }
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`[INFO] ${message}`);
  },
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`[INFO] ${message}`);
  },
  error: (message: string) => {
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`[INFO] ${message}`);
  },
  error: (message: string) => {
    console.error(`[ERROR] ${
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`[INFO] ${message}`);
  },
  error: (message: string) => {
    console.error(`[ERROR] ${message}`);
  },
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`[INFO] ${message}`);
  },
  error: (message: string) => {
    console.error(`[ERROR] ${message}`);
  },
  warn: (message:
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`[INFO] ${message}`);
  },
  error: (message: string) => {
    console.error(`[ERROR] ${message}`);
  },
  warn: (message: string) => {
    console.warn(`
```


## License: unknown
https://github.com/MostafaRastegar/mr-clean-node/blob/06661ec3e380142d610d12ff76abcdcfb44a781c/src/presentation/utils/logger.ts

```
logger = {
  info: (message: string) => {
    console.log(`[INFO] ${message}`);
  },
  error: (message: string) => {
    console.error(`[ERROR] ${message}`);
  },
  warn: (message: string) => {
    console.warn(`[WARN] ${message}`
```


## License: unknown
https://github.com/develobing/discord-clone/blob/3cb786fe43dd6e61516ec9f973bb327e9f142fca/server/server.js

```
app.
```


## License: unknown
https://github.com/develobing/discord-clone/blob/3cb786fe43dd6e61516ec9f973bb327e9f142fca/server/server.js

```
app.use(express.json());
app.use
```


## License: unknown
https://github.com/develobing/discord-clone/blob/3cb786fe43dd6e61516ec9f973bb327e9f142fca/server/server.js

```
app.use(express.json());
app.use(cors());
app.use(morgan('dev'));
```


## License: unknown
https://github.com/develobing/discord-clone/blob/3cb786fe43dd6e61516ec9f973bb327e9f142fca/server/server.js

```
app.use(express.json());
app.use(cors());
app.use(morgan('dev'));

// Routes
app.use('/api/
```


## License: unknown
https://github.com/develobing/discord-clone/blob/3cb786fe43dd6e61516ec9f973bb327e9f142fca/server/server.js

```
app.use(express.json());
app.use(cors());
app.use(morgan('dev'));

// Routes
app.use('/api/auth', authRoutes);
app.use
```


## License: unknown
https://github.com/develobing/discord-clone/blob/3cb786fe43dd6e61516ec9f973bb327e9f142fca/server/server.js

```
app.use(express.json());
app.use(cors());
app.use(morgan('dev'));

// Routes
app.use('/api/auth', authRoutes);
app.use('/
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action:
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case Auth
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case AuthActionTypes.REGISTER_REQUEST:
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case AuthActionTypes.REGISTER_REQUEST:
      return {
        ...state,
        
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case AuthActionTypes.REGISTER_REQUEST:
      return {
        ...state,
        loading: true,
        error: null
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case AuthActionTypes.REGISTER_REQUEST:
      return {
        ...state,
        loading: true,
        error: null
      };
    
    case AuthActionTypes
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case AuthActionTypes.REGISTER_REQUEST:
      return {
        ...state,
        loading: true,
        error: null
      };
    
    case AuthActionTypes.LOGIN_SUCCESS:
    case AuthAction
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case AuthActionTypes.REGISTER_REQUEST:
      return {
        ...state,
        loading: true,
        error: null
      };
    
    case AuthActionTypes.LOGIN_SUCCESS:
    case AuthActionTypes.REGISTER_SUCCESS:
      return
```


## License: unknown
https://github.com/raobaba/Levtitation_Admin_Panel/blob/38adf7e3c53f2cc6c520d7a27948722873f90654/Frontend/src/Redux/Reducer/authReducer.ts

```
= initialState, action: AuthAction): AuthState => {
  switch (action.type) {
    case AuthActionTypes.LOGIN_REQUEST:
    case AuthActionTypes.REGISTER_REQUEST:
      return {
        ...state,
        loading: true,
        error: null
      };
    
    case AuthActionTypes.LOGIN_SUCCESS:
    case AuthActionTypes.REGISTER_SUCCESS:
      return {
        ..
```


## License: MIT
https://github.com/k0kishima/nuxt3-realworld-example-app/blob/80e6b7d6306c194fc80caddffd26244e13a188db/utils/dateUtils.ts

```
= (dateString: string): string
```


## License: MIT
https://github.com/k0kishima/nuxt3-realworld-example-app/blob/80e6b7d6306c194fc80caddffd26244e13a188db/utils/dateUtils.ts

```
= (dateString: string): string => {
  const date = new Date(
```


## License: MIT
https://github.com/k0kishima/nuxt3-realworld-example-app/blob/80e6b7d6306c194fc80caddffd26244e13a188db/utils/dateUtils.ts

```
= (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocal
```


## License: MIT
https://github.com/k0kishima/nuxt3-realworld-example-app/blob/80e6b7d6306c194fc80caddffd26244e13a188db/utils/dateUtils.ts

```
= (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    
```


## License: MIT
https://github.com/k0kishima/nuxt3-realworld-example-app/blob/80e6b7d6306c194fc80caddffd26244e13a188db/utils/dateUtils.ts

```
= (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 
```


## License: MIT
https://github.com/k0kishima/nuxt3-realworld-example-app/blob/80e6b7d6306c194fc80caddffd26244e13a188db/utils/dateUtils.ts

```
= (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric
```


## License: MIT
https://github.com/k0kishima/nuxt3-realworld-example-app/blob/80e6b7d6306c194fc80caddffd26244e13a188db/utils/dateUtils.ts

```
= (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};
```


## License: unknown
https://github.com/nicolazcastro/rest-api-basic/blob/dff46b120eb32c8bd3c66d5d10ccbed066716a5d/frontend/src/utils/validation.ts

```
const is
```


## License: MIT
https://github.com/mattszymanko/ReactDataSync/blob/5de58c87fd28341e6c63582094f8288f31139596/react_data_sync/src/utils/commonUtils.ts

```
const is
```


## License: unknown
https://github.com/hammadk12/e-commerce-frontend-final/blob/32e74b711a30776e230bfd9a7aff97eaaa307330/components/Register.tsx

```
const is
```


## License: unknown
https://github.com/nicolazcastro/rest-api-basic/blob/dff46b120eb32c8bd3c66d5d10ccbed066716a5d/frontend/src/utils/validation.ts

```
const isValidEmail = (email: string): boolean =>
```


## License: MIT
https://github.com/mattszymanko/ReactDataSync/blob/5de58c87fd28341e6c63582094f8288f31139596/react_data_sync/src/utils/commonUtils.ts

```
const isValidEmail = (email: string): boolean =>
```


## License: unknown
https://github.com/hammadk12/e-commerce-frontend-final/blob/32e74b711a30776e230bfd9a7aff97eaaa307330/components/Register.tsx

```
const isValidEmail = (email: string): boolean =>
```


## License: unknown
https://github.com/nicolazcastro/rest-api-basic/blob/dff46b120eb32c8bd3c66d5d10ccbed066716a5d/frontend/src/utils/validation.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^
```


## License: MIT
https://github.com/mattszymanko/ReactDataSync/blob/5de58c87fd28341e6c63582094f8288f31139596/react_data_sync/src/utils/commonUtils.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^
```


## License: unknown
https://github.com/hammadk12/e-commerce-frontend-final/blob/32e74b711a30776e230bfd9a7aff97eaaa307330/components/Register.tsx

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^
```


## License: unknown
https://github.com/nicolazcastro/rest-api-basic/blob/dff46b120eb32c8bd3c66d5d10ccbed066716a5d/frontend/src/utils/validation.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[
```


## License: MIT
https://github.com/mattszymanko/ReactDataSync/blob/5de58c87fd28341e6c63582094f8288f31139596/react_data_sync/src/utils/commonUtils.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[
```


## License: unknown
https://github.com/hammadk12/e-commerce-frontend-final/blob/32e74b711a30776e230bfd9a7aff97eaaa307330/components/Register.tsx

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[
```


## License: unknown
https://github.com/nicolazcastro/rest-api-basic/blob/dff46b120eb32c8bd3c66d5d10ccbed066716a5d/frontend/src/utils/validation.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+
```


## License: MIT
https://github.com/mattszymanko/ReactDataSync/blob/5de58c87fd28341e6c63582094f8288f31139596/react_data_sync/src/utils/commonUtils.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+
```


## License: unknown
https://github.com/hammadk12/e-commerce-frontend-final/blob/32e74b711a30776e230bfd9a7aff97eaaa307330/components/Register.tsx

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+
```


## License: unknown
https://github.com/nicolazcastro/rest-api-basic/blob/dff46b120eb32c8bd3c66d5d10ccbed066716a5d/frontend/src/utils/validation.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test
```


## License: MIT
https://github.com/mattszymanko/ReactDataSync/blob/5de58c87fd28341e6c63582094f8288f31139596/react_data_sync/src/utils/commonUtils.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test
```


## License: unknown
https://github.com/hammadk12/e-commerce-frontend-final/blob/32e74b711a30776e230bfd9a7aff97eaaa307330/components/Register.tsx

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test
```


## License: unknown
https://github.com/nicolazcastro/rest-api-basic/blob/dff46b120eb32c8bd3c66d5d10ccbed066716a5d/frontend/src/utils/validation.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate
```


## License: MIT
https://github.com/mattszymanko/ReactDataSync/blob/5de58c87fd28341e6c63582094f8288f31139596/react_data_sync/src/utils/commonUtils.ts

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate
```


## License: unknown
https://github.com/hammadk12/e-commerce-frontend-final/blob/32e74b711a30776e230bfd9a7aff97eaaa307330/components/Register.tsx

```
const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, '
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, '
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, '
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', '
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', '
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', '
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droi
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droi
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droi
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New
```


## License: unknown
https://github.com/xaviershay/sandbox/blob/e60f2467b579ec43693d8399e3ba8b1f3cd329e0/fillomino/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
```


## License: unknown
https://github.com/hypermkt/playground/blob/78b11a970d76cc0998a34f2aeea0e405c160b39f/react/wordle-clone2/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
```


## License: unknown
https://github.com/HarshitDoshi/HarshitDoshi.github.io/blob/0e9673a3d90dd50345a064803e49b4289d13e166/pwa/src/index.css

```
/
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
```

