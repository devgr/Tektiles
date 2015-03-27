/* 
  _______        _   _ _         _____                                  _             
 |__   __|      | | (_) |       / ____|                                (_)            
    | | _____  _| |_ _| | ___  | |     ___  _ __ ___  _ __   __ _ _ __  _  ___  _ __  
    | |/ _ \ \/ / __| | |/ _ \ | |    / _ \| '_ ` _ \| '_ \ / _` | '_ \| |/ _ \| '_ \ 
    | |  __/>  <| |_| | |  __/ | |___| (_) | | | | | | |_) | (_| | | | | | (_) | | | |
    |_|\___/_/\_\\__|_|_|\___|  \_____\___/|_| |_| |_| .__/ \__,_|_| |_|_|\___/|_| |_|
               | |/ /                                | |                              
               | ' / ___ _   _ ______ __ _  ___ _ __ |_|                              
               |  < / _ \ | | |______/ _` |/ _ \ '_ \                                 
               | . \  __/ |_| |     | (_| |  __/ | | |                                
               |_|\_\___|\__, |      \__, |\___|_| |_|                                
                          __/ |       __/ |                                           
                         |___/       |___/                                            
 
 
  ___                                              _   ___           _   ___     _ _         
 | _ \_ _ ___  __ _ _ _ __ _ _ __  _ __  ___ _ _  (_) | _ \__ _ _  _| | | __|  _| | |___ _ _ 
 |  _/ '_/ _ \/ _` | '_/ _` | '  \| '  \/ -_) '_|  _  |  _/ _` | || | | | _| || | | / -_) '_|
 |_| |_| \___/\__, |_| \__,_|_|_|_|_|_|_\___|_|   (_) |_| \__,_|\_,_|_| |_| \_,_|_|_\___|_|  
              |___/                                                                           
 
 
 */



using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Security.Cryptography;
using System.IO;
using System.Drawing.Printing;


namespace WindowsFormsApplication3
{
    public partial class Form1 : Form
    {

        private static Random random = new Random((int)DateTime.Now.Ticks);
        private string RandomString(int size)
        {
            StringBuilder builder = new StringBuilder();
            char ch;
            for (int i = 0; i < size; i++)
            {
                ch = Convert.ToChar(Convert.ToInt32(Math.Floor(26 * random.NextDouble() + 65)));
                builder.Append(ch);
            }

            return builder.ToString();
        }

        static string GetMd5Hash(MD5 md5Hash, string input)
        {

            // Convert the input string to a byte array and compute the hash. 
            byte[] data = md5Hash.ComputeHash(Encoding.UTF8.GetBytes(input));

            // Create a new Stringbuilder to collect the bytes 
            // and create a string.
            StringBuilder sBuilder = new StringBuilder();

            // Loop through each byte of the hashed data  
            // and format each one as a hexadecimal string. 
            for (int i = 0; i < data.Length; i++)
            {
                sBuilder.Append(data[i].ToString("x2"));
            }

            // Return the hexadecimal string. 
            return sBuilder.ToString();
        }

        static bool VerifyMd5Hash(MD5 md5Hash, string input, string hash)
        {
            // Hash the input. 
            string hashOfInput = GetMd5Hash(md5Hash, input);

            // Create a StringComparer an compare the hashes.
            StringComparer comparer = StringComparer.OrdinalIgnoreCase;

            if (0 == comparer.Compare(hashOfInput, hash))
            {
                return true;
            }
            else
            {
                return false;
            }
        }



        public Form1()
        {
            InitializeComponent();
        }



        private void button1_Click(object sender, EventArgs e)
        {

            if (textBox1.Text != "")
            {
                //string[] key = new string[Convert.ToInt32(textBox1.Text) * 2];
                List<string> key = new List<string>();
                string[] keyList = new string[Convert.ToInt32(textBox1.Text) * 2];

                if (textBox1.Text.All((Char.IsDigit)))
                {


                    for (int i = 0; i < Convert.ToInt32(textBox1.Text) * 2; i++)
                    {

                        //create randomly generated string, ie salt
                        string rand = RandomString(5);

                        //make salt lower case
                        rand = rand.ToLower();

                        //create MD5 hash object 
                        MD5 md5Hash = MD5.Create();

                        //Generate hash from random string
                        string hash = GetMd5Hash(md5Hash, rand);

                        //convert hash string to a a string array
                        string[] hashArray = hash.Select(c => c.ToString()).ToArray();

                        //create a list and initialize it with hashArray
                        List<string> list = new List<string>(hashArray);

                        //insert salt at positions 0,5,10,15,20 with salt positions 0,1,2,3,4 respectively
                        list.Insert(0, rand[0].ToString());
                        list.Insert(5, rand[1].ToString());
                        list.Insert(10, rand[2].ToString());
                        list.Insert(15, rand[3].ToString());
                        list.Insert(20, rand[4].ToString());

                        //convert list to string and store in result
                        StringBuilder builder = new StringBuilder();
                        foreach (string pkey in list) // Loop through all strings
                        {
                            builder.Append(pkey).Append(""); // Append string to StringBuilder
                        }
                        string result = builder.ToString();

                        //add result to string array keyList
                        keyList[i] = result;
                        i++;
                        //insert space for formatting reasons
                        keyList[i] = "\n";




                    }
                    //save keys to file at path:
                    string path = @"C:\Companion\";

                    // if dir exists write, else create dir then write.
                    if (Directory.Exists(path))
                    {

                        System.IO.File.WriteAllLines(@"C:\Companion\ProductKeys.txt", keyList);

                        //create a new print button at point 233,12
                        Button print = new Button();
                        print.Text = "Print";
                        print.Location = new Point(233, 12);
                        print.Click += print_Click;
                        ToolTip toolTip5 = new ToolTip();
                        toolTip5.SetToolTip(print, "Click to print generated keys.");
                        tabPage1.Controls.Add(print);




                    }
                    else
                    {
                        DirectoryInfo di = Directory.CreateDirectory(path);
                        System.IO.File.WriteAllLines(@"C:\Companion\ProductKeys.txt", keyList);

                        //create a new print button at point 233,12
                        Button print = new Button();
                        print.Text = "Print";
                        print.Location = new Point(233, 12);
                        ToolTip toolTip5 = new ToolTip();
                        toolTip5.SetToolTip(print, "Click to print generated keys.");
                        tabPage1.Controls.Add(print);

                    }

                    //alert done 
                    MessageBox.Show("The license keys have been generated.");

                }
                else
                {
                    MessageBox.Show("Error: Please enter only numbers");
                }
            }
            else
            {

                MessageBox.Show("Error: Please enter the quantity of keys to be generated.");
            }
        }

        Font printFont = new Font("Arial", 10);
        StreamReader Printfile;
        public void print_Click(object sender, EventArgs e)
        {
            using (Printfile = new StreamReader("c:\\Companion\\ProductKeys.txt"))
            {
                try
                {
                    PrintDocument docToPrint = new PrintDocument();
                    docToPrint.DocumentName = "Password"; //Name that appears in the printer queue
                    docToPrint.PrintPage += (s, ev) =>
                    {
                        float linesPerPage = 10;
                        float yPos = 0;
                        int count = 0;
                        float leftMargin = ev.MarginBounds.Right / 2;
                        float topMargin = ev.MarginBounds.Top;
                        string line = null;

                        // Calculate the number of lines per page.
                        linesPerPage = ev.MarginBounds.Height / printFont.GetHeight(ev.Graphics);
                        StringFormat stringFormat = new StringFormat();
                        stringFormat.Alignment = StringAlignment.Center;
                        stringFormat.LineAlignment = StringAlignment.Center;

                        // Print each line of the file. 
                        while (count < linesPerPage && ((line = Printfile.ReadLine()) != null))
                        {
                            yPos = topMargin + (count * printFont.GetHeight(ev.Graphics));
                            ev.Graphics.DrawString(line, printFont, Brushes.Black, leftMargin, yPos, stringFormat);
                            ev.Graphics.DrawString(line, printFont, Brushes.Black, leftMargin, yPos, stringFormat);


                            count++;
                        }

                        // If more lines exist, print another page. 
                        if (line != null)
                            ev.HasMorePages = true;
                        else
                            ev.HasMorePages = false;
                    };
                    //docToPrint.PrintController.IsPreview = true;
                    docToPrint.Print();

                }
                catch (System.Exception f)
                {
                    MessageBox.Show(f.Message);
                }
            }
        }

        //
        /*private void printDocument1_PrintPage(object sender, System.Drawing.Printing.PrintPageEventArgs ev)
        {
            float linesPerPage = 0;
            float yPos = 0;
            int count = 0;
            float leftMargin = ev.MarginBounds.Left;
            float topMargin = ev.MarginBounds.Top;
            string line = null;
            StringFormat drawFormat = new StringFormat();
            

            // Calculate the number of lines per page.
            linesPerPage = ev.MarginBounds.Height /
               printFont.GetHeight(ev.Graphics);

            // Print each line of the file. 
            while (count < linesPerPage &&
               ((line = fileToPrint.ReadLine()) != null))
            {
                yPos = topMargin + (count *
                   printFont.GetHeight(ev.Graphics));
                ev.Graphics.DrawString(line, printFont, Brushes.Black, leftMargin, yPos, drawFormat);
                count++;
            }

            // If more lines exist, print another page. 
            if (line != null)
                ev.HasMorePages = true;
            else
                ev.HasMorePages = false;
        }*/


        //Actions for Program launch
        private void Form1_Load(object sender, EventArgs e)
        {
            tabPage1.Text = "Generate";
            tabPage2.Text = "Verify Key";
            toolTip1.SetToolTip(Generate, "Click to Generate Keys.");
            toolTip2.SetToolTip(textBox1, "Enter number of keys to be generated.");
            toolTip3.SetToolTip(button1, "Click to verify a single key");
            toolTip4.SetToolTip(textBox2, "Enter a license key to verify.");

        }

        private void splitContainer1_Panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void tabPage1_Click(object sender, EventArgs e)
        {

        }



        //verify Key on button1_Click_1 event
        private void button1_Click_1(object sender, EventArgs e)
        {
            if (textBox2.Text != "")
            {
                int length = textBox2.Text.Length;
                if (textBox2.Text.Length == 37)
                {
                    string[] key = new string[5];
                    string hash;
                    string salt;

                    string[] array = new string[1];
                    array[0] = textBox2.Text;
                    List<string> list = textBox2.Text.Select(c => c.ToString()).ToList();

                    //extract the salt and hash from the key 
                    int saltPos = 0;
                    for (int i = 0; i < 37; i++)
                    {

                        if (i == 0 || i == 5 || i == 10 || i == 15 || i == 20)
                        {
                            key[saltPos] = textBox2.Text.Substring(i, 1);
                            
                            saltPos++;
                        }
                       
                    }

                    //Remove salt leaving hash ( The indexes change as you remove)
                    list.RemoveAt(0);
                    list.RemoveAt(4);
                    list.RemoveAt(8);
                    list.RemoveAt(12);
                    list.RemoveAt(16);

                    //create string from list
                    StringBuilder builderHash = new StringBuilder();
	                foreach (string c in list) // Loop through all strings
	                {
	                    builderHash.Append(c).Append(""); // Append string to StringBuilder
	                }
                    hash = builderHash.ToString();

                    //create string from key
                    StringBuilder builderKey = new StringBuilder();
                    foreach (string c in key) // Loop through all strings
                    {
                        builderKey.Append(c).Append(""); // Append string to StringBuilder
                    }
                    salt = builderKey.ToString();
                    

                    // hash[0] = textBox2.Text.Substring(1, 5);

                    
                     MD5 md5Hash = MD5.Create();
                    
                     //Generate hash from keyCode
                     string verify = GetMd5Hash(md5Hash, salt);
                     
                     //validate hash
                     if (verify == hash)
                     {
                         //post valid message 
                         label3.Text = "Valid Key";
                         MessageBox.Show("Valid Key!");
                     }
                     else
                     {
                         //post invalid message
                         label3.Text = "Invalid Key";
                         MessageBox.Show("Invalid Key!");
                     }
                 }
                 else
                 {
                     label3.Text = "Invalid Key";
                     MessageBox.Show("Invalid Key!");
                 }

             }
             else
             {
                 MessageBox.Show("Error: Please enter a key.");
             }

          

                }






            }
        }
    

