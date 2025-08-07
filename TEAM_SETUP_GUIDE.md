# 🚀 AtPoE Multi-Bundle System - Team Setup Guide

## 📋 **What You Need (Already Installed)**
✅ Python3  
✅ pip3  
✅ Streamlit  

## 🎯 **What This System Does**
Create layered curve compositions by adding different graphics bundles (colors, line styles) one at a time. Each new bundle continues from where the previous one left off.

---

## 📥 **Step 1: Download the Files**

### **Option A: If you have the repository**
```bash
git clone [repository-url]
cd closed_curve_copy\ copy
```

### **Option B: If you need the files manually**
Download these files to a folder:
- `atpoe_multi_bundle_simple.py`
- `graphics_bundle.py` 
- `collision_detector.py`

---

## 🔧 **Step 2: Install Dependencies**

Open your terminal/command prompt and run:

```bash
pip3 install streamlit pillow
```

**Wait for it to finish** - you'll see "Successfully installed..." messages.

---

## 🚀 **Step 3: Run the System**

### **Navigate to your folder:**
```bash
cd [path-to-your-folder]
```

### **Start the application:**
```bash
streamlit run atpoe_multi_bundle_simple.py
```

### **What happens:**
- Terminal will show: "You can now view your Streamlit app in your browser"
- **Local URL**: http://localhost:8501
- **Network URL**: http://[your-ip]:8501

### **Open your browser:**
- Go to: **http://localhost:8501**
- You should see the AtPoE interface

---

## 🎨 **Step 4: How to Use (Simple Steps)**

### **First Bundle:**
1. **Select Bundle**: Choose "Classic Black" from dropdown
2. **Set Parameters**:
   - Number of Curves: 6
   - Error Level: 1.5
   - Curve Distance: 8
3. **Click**: "➕ Add Bundle"
4. **See**: Black curves appear

### **Second Bundle:**
1. **Select Bundle**: Choose "Bold Orange" from dropdown
2. **Set Parameters**:
   - Number of Curves: 3
   - Error Level: 1.0
   - Curve Distance: 8
3. **Click**: "➕ Add Bundle"
4. **See**: Orange curves continue from where black ones ended

### **Continue Adding Bundles:**
- Repeat the process with different bundles
- Each new bundle continues from the previous one
- Try different colors and parameters

### **Download Your Work:**
- Click "📥 Download PNG" to save your composition

---

## 🎯 **Quick Test (5 Minutes)**

### **Try This Sequence:**
1. **Bundle 1**: Classic Black (6 curves, Error 1.5)
2. **Bundle 2**: Bold Orange (3 curves, Error 1.0)  
3. **Bundle 3**: Classic Blue (4 curves, Error 1.8)
4. **Bundle 4**: Thin Gray (2 curves, Error 1.0)

**Result**: A layered composition with 4 different styles!

---

## 🛠️ **Troubleshooting**

### **Problem**: "Module not found" error
**Solution**: Make sure you're in the right folder with all the files

### **Problem**: "Port already in use" 
**Solution**: 
```bash
streamlit run atpoe_multi_bundle_simple.py --server.port 8502
```

### **Problem**: Blank screen
**Solution**: 
1. Check the terminal for error messages
2. Try refreshing the browser
3. Make sure all files are in the same folder

### **Problem**: Can't see the interface
**Solution**: 
1. Make sure you're going to http://localhost:8501
2. Check if your browser is blocking the page
3. Try a different browser

---

## 📁 **File Structure**

Your folder should look like this:
```
your-folder/
├── atpoe_multi_bundle_simple.py    ← Main application
├── graphics_bundle.py              ← Graphics system
├── collision_detector.py           ← Collision detection
└── TEAM_SETUP_GUIDE.md            ← This guide
```

---

## 🎨 **Available Graphics Bundles**

- **Classic Black**: Clean, professional (2px)
- **Classic Red**: Bold emphasis (2px)
- **Classic Blue**: Calming base (2px)
- **Bold Orange**: Strong impact (4px)
- **Bold Brown**: Rich separator (4px)
- **Thin Gray**: Subtle details (1px)
- **Thin Magenta**: Fine accents (1px)

---

## 📊 **Parameter Guide**

### **Number of Curves**: 1-20
- **1-3**: Minimal
- **4-8**: Balanced
- **9-15**: Complex
- **16-20**: Very dense

### **Error Level**: 0.0-5.0
- **0.0-1.0**: Precise, geometric
- **1.1-2.5**: Natural, organic
- **2.6-4.0**: Expressive, artistic
- **4.1-5.0**: Very loose, abstract

### **Curve Distance**: 3-20
- **3-6**: Tight, dense
- **7-12**: Balanced spacing
- **13-17**: Open, airy
- **18-20**: Very open

---

## 🎯 **Creative Tips**

### **Start Simple:**
- Begin with 1-2 bundles
- Use classic, solid styles first
- Add complexity gradually

### **Use Separators:**
- Bold bundles (Orange, Brown) make great separators
- Use them between different style groups
- 1-2 thick curves work well

### **Vary Parameters:**
- Don't use the same parameters for every bundle
- Experiment with different error levels
- Try different curve counts

---

## 🚀 **Quick Commands Reference**

### **Start the app:**
```bash
streamlit run atpoe_multi_bundle_simple.py
```

### **Start on different port:**
```bash
streamlit run atpoe_multi_bundle_simple.py --server.port 8502
```

### **Stop the app:**
- Press `Ctrl+C` in the terminal

---

## 📞 **Need Help?**

### **Check the terminal** for error messages
### **Make sure all files** are in the same folder
### **Try refreshing** the browser
### **Restart the app** if needed

---

## 🎉 **You're Ready!**

1. ✅ **Files downloaded**
2. ✅ **Dependencies installed** 
3. ✅ **App running**
4. ✅ **Browser open**
5. 🎨 **Start creating!**

**Happy curve generating! 🎨**
