# คู่มือการติดตั้ง CIS-Curriculum Checking System

ในการใช้งาน จะต้องควบคู่ไปกับโปรแกรม MySQL Workbench 8.0 เนื่องจากระบบมีการเชื่อมต่อกับฐานข้อมูลภายในโปรแกรมนี้ โดยสามารถดาวน์โหลดได้ฟรี

สำหรับผู้ที่ต้องการจะนำไปใช้ ขอให้ศึกษารายละเอียดการใช้งานดังต่อไปนี้
1. ส่วนประกอบใน Directory ซึ่งจะใช้ Branch <code>main</code> ในการอัปเดตไฟล์เป็นหลัก

    - ไฟล์ <code>main.py</code> ซึ่งเป็นไฟล์หลักในการรันงาน
    - <code>requirements.txt</code> สำหรับการติดตั้ง Library ที่จำเป็นต่อการใช้งาน
    - <code>subjects_text.csv</code> และ <code>curriculum_format-DSI.csv</code> ใช้สำหรับการนำเข้าข้อมูลรายวิชาและแผนการเรียนลงใน Database
    - โฟลเดอร์ website จะรวบรวมไฟล์ที่ใช้รันหน้าเว็บต่างๆ รวมถึงการทำ Authentication และมี templates ที่รวบรวมหน้าเว็บทุกหน้าที่เกี่ยวข้องกับระบบ และ static ที่เก็บรูปภาพต่างๆ

2. การรัน Project เบื้องต้น
        
    เบื้องต้นผู้ใช้จะต้องสร้าง Database ในโปรแกรม MySQL Workbench 8.0 ก่อน โดยใช้ชื่อตามที่ผู้ใช้ต้องการ แต่จะต้องเหมือนกันกับในไฟล์ <code>__init__.py</code> ที่มีการระบุ Database ที่จะทำการเชื่อมต่อ รวมถึง Username และ Password จะต้องเหมือนกันด้วย 
    
    จากนั้นให้ผู้ใช้ทำการรันคำสั่ง <code>git clone \<link from GitHub\></code> เพื่อทำการดึงมาใส่ในโฟลเดอร์ของผู้ใช้ได้ และทำการกดรันหน้า <code>main.py</code> ได้เลย ซึ่งในที่นี้ขอแนะนำให้ใช้โปรแกรม Visual Studio Code ในการรัน ซึ่งในตอนแรกจะยังไม่มีข้อมูลอยู่ใน Database เมื่อทำการรันแล้วจะมีการนำข้อมูลเบื้องต้นเข้าใน Database ได้แก่ ข้อมูลรายวิชา ข้อมูลแผนการเรียน ข้อมูลหลักสูตร และข้อมูลประเภทรายวิชา โดยมีการกำหนการนำเข้าข้อมูลอยู่ในฟังก์ชัน <code>add_data</code> ในไฟล์ <code>\_\_init\_\_.py</code> 
