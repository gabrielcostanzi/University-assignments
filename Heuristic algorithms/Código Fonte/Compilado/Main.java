import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;

/**
 * RA112649 - Thiago Yuji Yoshimura Yamamoto
 * RA102573 - Gabriel Henrique Costanzi
 */

//Cada vértice possui o seu identificador e as posições (x, y)
//calculaDistancia esta presente na classe vertice, pois calcula-se a distância do vértice atual até um outro diferente
class Vertice {
    public int identificador;
    public int x, y;
    public boolean visitado;

    public Vertice(){
        super();
    }

    public Vertice (int identificador, int x, int y){
        this.identificador = identificador;
        this.x = x;
        this.y = y;
    }

    public int calculaDistancia(Vertice verticeProximo){
        int x = verticeProximo.x - this.x;
        int y = verticeProximo.y - this.y;
        return (int) Math.sqrt(Math.pow(x,2) + Math.pow(y,2));
    }
}

class Main {

    //Método para verificar se a saída resulta em um ciclo
    private static boolean verificaCaminho(ArrayList<Vertice> saidaOut){
        for(int i = 0; i < saidaOut.size()-1; i++){
            if(saidaOut.get(i).visitado){
                return false;
            }else{
                saidaOut.get(i).visitado = true;
            }
        }
        if(saidaOut.get(saidaOut.size()-1) == saidaOut.get(0)){
            return true;
        }else{
            return false;
        }
    }

    //Função para calcular o pesoTotal com custo O(n)
    private static int calculaPesoTotal(ArrayList<Vertice> saidaOut){
        int pesoTotal = 0;
        for(int i = 0; i < saidaOut.size()-1; i++) pesoTotal = pesoTotal + saidaOut.get(i).calculaDistancia(saidaOut.get(i+1));
        return pesoTotal;
    }

    //Função para calcular o peso de 3 arestas
    //Usado para calcular o peso das arestas após as trocas
    private static int calculaPeso(ArrayList<Vertice> saidaOut, int a, int b, int c, int d, int e, int f){
        return (saidaOut.get(a).calculaDistancia(saidaOut.get(b)) + saidaOut.get(c).calculaDistancia(saidaOut.get(d)) + saidaOut.get(e).calculaDistancia(saidaOut.get(f)));
    }

    //Algoritmo Construtivo Vizinho mais próximo
    //Insere na lista da solução inicial (saidaOut) o vértice mais próximo do último vértice da lista
    private static void construtivoVizinhoProximo(ArrayList<Vertice> listVertice, ArrayList<Vertice> saidaOut){
        /**Inicializa:
         * i --> qual vertice começara (gerado o valor aleatoriamente de acordo com a quantidade de vértices)
         * menor --> menor peso do vértice (da posição i na lista) para o j
         */
        int menor = Integer.MAX_VALUE;
        int menorB = 0;     
        int A = new Random().nextInt(listVertice.size()-1);
        Vertice vertice = listVertice.get(A);
        Vertice verticeProximo = new Vertice();
        listVertice.remove(A);
        saidaOut.add(vertice);
        while(!listVertice.isEmpty()){
            for(int B = 0; B < listVertice.size(); B++){
                verticeProximo = listVertice.get(B);
                int peso = vertice.calculaDistancia(verticeProximo);
                if(peso < menor){
                    menor = peso;
                    menorB = B;
                }               
            }
            vertice = listVertice.get(menorB);
            saidaOut.add(vertice);           
            listVertice.remove(menorB);
            menor = Integer.MAX_VALUE;
        }
        saidaOut.add(saidaOut.get(0));
    }
    
    //Algoritmo Construtivvo Inserção Rápida
    //Semelhante ao Vizinho mais próximo, porém a inserção na lista pode ser no meio
    private static void construtivoInsercaoRapida(ArrayList<Vertice> listVertice, ArrayList<Vertice> saidaOut){
        int menor = Integer.MAX_VALUE;
        int random;
        int i;

        //Seleciona um vértice aleatório
        int A = new Random().nextInt(listVertice.size()-1);
        Vertice vertice = listVertice.get(A);
        listVertice.remove(A);
        saidaOut.add(vertice);

        while(!listVertice.isEmpty()){
            int posicaoSaidaOut = 0;
            random = new Random().nextInt(listVertice.size());
            Vertice verticek = listVertice.get(random);
            listVertice.remove(random);
            for(i = 0; i < saidaOut.size()-1; i++){
                int custo = saidaOut.get(i).calculaDistancia(verticek);
                if(custo < menor){
                    menor = custo;
                    posicaoSaidaOut = i;
                }
            }
            saidaOut.add(posicaoSaidaOut, verticek);         
            menor = Integer.MAX_VALUE;
        }
        saidaOut.add(saidaOut.get(0));

    }

    //Método para trocar os vértices de posição e inverter a lista entre eles
    private static void swap2OPT(ArrayList<Vertice> saidaOPT, int verticeB, int i){
        Collections.swap(saidaOPT, verticeB, i);
        int a = verticeB+1;
        int b = i-1;
        while(a < b){
            Collections.swap(saidaOPT, a, b);
            a++;
            b--;
        }
    }

    //Algoritmo Melhoratio 2-OPT
    //Método usado: First Improvement
    //Método para acelerar o algoritmo: Fator de Aceleração sem restrição
    /** Fator de Aceleração:
     *  Este método tem como objetivo ajudar o algoritmo encontrar o vizinho otimizado mais rapidamente, por causa da verificação sequencial dos vizinhos
     *  Quanto mais restrições o método possui menos vizinhos serão comparados
     *  O 2-OPT não possui nenhuma restrição, voltando a aresta pivô AB para o inicio caso não seja encontrado uma otimização
     * 
     *  Resultado: observamos que o algoritmo encontra a solução ótima local mais rapidamente
     *  Obs: o método foi apelidado para facilitar a sua citação no relatório, pois não encontramos um método parecido na internet.
     */
    private static ArrayList<Vertice> melhorativo2OPT(ArrayList<Vertice> saidaOut, PrintWriter buffeWriter, Double valorOtimo){
        boolean temOPT = true;
        ArrayList<Vertice> saidaOPT = new ArrayList<>(saidaOut);
        int melhoraAB = 0;
        int paradaAB = saidaOPT.size()-1;
        int ciclo = 0;
        int a = 0;

        boolean stop = false;

        long inicio = System.currentTimeMillis();
        long fim = 0;
    
        while(temOPT && !stop){
            paradaAB = saidaOPT.size()-1;
            temOPT = false;
            for(int verticeA = melhoraAB; verticeA < paradaAB && !temOPT && !stop; verticeA++){
                //Condição para retornar a posição do verticeA para 0
                //Isso só acontece quando não é encontrado nenhuma solução do vérticeA (posição da última melhoria) até o fim da lista
                if(melhoraAB > 0 && verticeA == saidaOPT.size()-2){
                    paradaAB = melhoraAB;
                    verticeA = 0;
                }
                int verticeB = verticeA + 1;
                for(int i = verticeB+1; i < saidaOPT.size()-1 && !temOPT && !stop; i++){
                    int j = i+1;
                    if(j != verticeA){
                        int menor = saidaOPT.get(verticeA).calculaDistancia(saidaOPT.get(verticeB)) + saidaOPT.get(i).calculaDistancia(saidaOPT.get(j));
                        int custo = (saidaOPT.get(verticeA).calculaDistancia(saidaOPT.get(i)) + saidaOPT.get(verticeB).calculaDistancia(saidaOPT.get(j)));
                        if(custo < menor){  
                            int antes = calculaPesoTotal(saidaOPT);
                            swap2OPT(saidaOPT, verticeB, i);     
                            temOPT = true;
                            int depois = calculaPesoTotal(saidaOPT);
                            buffeWriter.println(ciclo++ + "," + (antes - depois) + "," + depois);
                            //Muda a posição do verticeA para o próximo ciclo
                            melhoraAB = verticeA;
                        }   
                        
                        
                        a++;
                    }
                }
            }         
        }
        fim = System.currentTimeMillis();
        int pesoTotal = calculaPesoTotal(saidaOPT);
        System.out.println("\tPeso: " + pesoTotal);
        System.out.println("\tPrecisao: " + valorOtimo/pesoTotal);
        System.out.println("\tIteracoes: " + a);
        System.out.println("\tTempo: " + (fim-inicio) + "ms");
        buffeWriter.close();
        return saidaOPT;
    }

    //Algoritmo Melhorativo 3-OPT
    //Método usado: First Improvement
    //Método para acelerar o algoritmo: Fator de Aceleração com restrição nas arestas AB e EF
    private static ArrayList<Vertice> melhorativo3OPT(ArrayList<Vertice> saidaOut, PrintWriter buffeWriter, Double valorOtimo){
        boolean temOPT = true;
        int A, B, C, D, E , F;
        int ciclo = 0;
        int paradaAB = saidaOut.size()-5;
        int paradaCD = saidaOut.size()-3;
        int paradaEF = saidaOut.size()-1;
        int melhoraAB = 0;
        int melhoraCD = 2;
        int melhoraEF = 4;
        boolean stop = false;
        int a = 0;

        long inicio = System.currentTimeMillis();
        long fim = 0;

        while (temOPT && !stop){
            paradaAB = saidaOut.size()-5;
            temOPT = false;
            //A aresta AB não retorna para inicio (não possui a condição "if" presente no algoritmo 2-OPT)
            for (A=melhoraAB; A < paradaAB && !temOPT && !stop; A++){             
                B = A + 1;
                if(B >= melhoraCD) melhoraCD = B + 1;
                paradaCD = saidaOut.size()-3;
                //A aresta CD sem restrição, retornando para o inicio
                for(C=melhoraCD; C < paradaCD && !temOPT && !stop;C++){                 
                    if(melhoraCD > (B + 1) && C == saidaOut.size()-4){
                        paradaCD = melhoraCD;
                        C = B + 1;
                    }
                    D = C + 1;
                    if(D >= melhoraEF) melhoraEF = D + 1;
                    paradaEF = saidaOut.size()-1;
                    //A aresta EF retorna para a posição equivalente ao tamanho entre as arestas CD e EF
                    for(E = melhoraEF; E < paradaEF && !temOPT && !stop;E++){
                        F = E + 1;
                        if(F != A){
                            //O método 3-OPT pode ser simplificado em duas trocas 2-OPT (método swap2OPT())
                            int antes = 0;                
                            int menor = saidaOut.get(A).calculaDistancia(saidaOut.get(B)) + saidaOut.get(C).calculaDistancia(saidaOut.get(D)) + saidaOut.get(E).calculaDistancia(saidaOut.get(F));
                            if(calculaPeso(saidaOut, A,D,E,C,B,F) < menor){ //caso 1 A,D,E,C,B,F
                                antes = calculaPesoTotal(saidaOut);
                                swap2OPT(saidaOut, D, E);
                                swap2OPT(saidaOut, B, E);
                                temOPT = true;
                            }else
                            if(calculaPeso(saidaOut, A,E,D,B,C,F) < menor){ //caso 2 A,E,D,B,C,F
                                antes = calculaPesoTotal(saidaOut);
                                swap2OPT(saidaOut, B, C);
                                swap2OPT(saidaOut, B, E);
                                temOPT = true;
                            }else
                            if(calculaPeso(saidaOut, A,C,B,E,D,F) < menor){ //caso 3 A,C,B,E,D,F
                                antes = calculaPesoTotal(saidaOut);
                                swap2OPT(saidaOut, D, E);
                                swap2OPT(saidaOut, B, C);
                                temOPT = true;
                            }else
                            if(calculaPeso(saidaOut, A,D,E,B,C,F) < menor){ //caso 4 A,D,E,B,C,F
                                antes = calculaPesoTotal(saidaOut);
                                swap2OPT(saidaOut, D, E);
                                swap2OPT(saidaOut, B, C);
                                swap2OPT(saidaOut, B, E);
                                temOPT = true;
                            }else
                            if(calculaPeso(saidaOut, A, C, B, D, E, F) < menor){   //B <--> C
                                antes = calculaPesoTotal(saidaOut);
                                swap2OPT(saidaOut, B, C);
                                temOPT = true;
                            } else
                            if(calculaPeso(saidaOut, A, E, D, C, B, F) < menor){  //B <--> E
                                antes = calculaPesoTotal(saidaOut);
                                swap2OPT(saidaOut, B, E);
                                temOPT = true;
                            }else
                            if(calculaPeso(saidaOut, A, B, C, E, D, F) < menor){  //D <--> E
                                antes = calculaPesoTotal(saidaOut);
                                swap2OPT(saidaOut, D, E);
                                temOPT = true;
                            }

                            if(temOPT){                      
                                int depois = calculaPesoTotal(saidaOut);
                                buffeWriter.println(ciclo++ + "," + (antes - depois) + "," + depois);
                                melhoraAB = A;
                                melhoraCD = C;
                                melhoraEF = D + (E - D)/10;   
                            }                          
                            a++;
                        }
                    }

                }

            }          
        }
        fim = System.currentTimeMillis();
        int pesoTotal = calculaPesoTotal(saidaOut);
        System.out.println("\tPeso: " + pesoTotal);
        System.out.println("\tPrecisao: " + valorOtimo/pesoTotal);
        System.out.println("\tIteracoes: " + a);
        System.out.println("\tTempo: " + (fim-inicio) + "ms");
        buffeWriter.close();
        return saidaOut;
    }

    //Criação das tabelas em .txt de cada combinação dos algoritmos
    //Utilizamos o arquivo para gerar um gráfico no excel e apresenta-lo no relatório
    private static PrintWriter criaTabela(String nomeArquivo, String entrada){
        try{
            FileWriter leitor = new FileWriter("./tabelas/".concat(entrada.concat("-").concat(nomeArquivo.concat(".txt"))));
            PrintWriter bufferWriter = new PrintWriter(leitor);
            bufferWriter.println("Ciclo,Melhoria,Otimizado");
            return bufferWriter;
        }catch(IOException ex){
            System.out.println("Falha na leitura do arquivo");
            System.exit(0);
            return null;
        }
    } 

    public static void main(String[] args) throws Exception {
        ArrayList<Vertice> listVertice = new ArrayList<Vertice>();
        ArrayList<Vertice> saidaVP = new ArrayList<Vertice>();
        ArrayList<Vertice> saidaIR = new ArrayList<Vertice>();
        HashMap<String,Double> resultado = new HashMap<String,Double>();
        
        String entrada = args[0];
        
        Scanner readerOtimo = new Scanner(new FileReader("./resultados.txt"));
        Scanner reader = new Scanner(new FileReader("./entradas/".concat(entrada).concat(".tsp")));

        //Leitura do arquivo resultados.txt, para calcular a precisão dos algoritmos
        while(readerOtimo.hasNextLine()){
            String[] linha = readerOtimo.nextLine().split("[:]");
            resultado.put(linha[0],Double.parseDouble(linha[1]));
        }
        readerOtimo.close();

        //Pula a leitura das 6 primeiras linhas
        while(!reader.hasNextInt()) reader.nextLine();
        
        while(reader.hasNextInt()){
            int identificador;
            int x, y;

            identificador = reader.nextInt();
            x = reader.nextInt();
            y = reader.nextInt();

            listVertice.add(new Vertice(identificador, x, y));
        }

        reader.close();

        //Execução dos algoritmos construtivos          
        System.out.println("-------------- Construtivos --------------");
        construtivoVizinhoProximo(new ArrayList<Vertice>(listVertice), saidaVP);
        int pesoVP = calculaPesoTotal(saidaVP);
        System.out.println("\nVizinho Proximo: " + pesoVP);
        construtivoInsercaoRapida(listVertice, saidaIR);
        int pesoIR = calculaPesoTotal(saidaIR);
        System.out.println("Insercao Rapida : " + pesoIR);

        //Guarda os valores dos construtivos em um arquivo .txt
        PrintWriter bufferConstrutivo = criaTabela("Construtivos",entrada);
        bufferConstrutivo.println("Vizinho Proximo: " + pesoVP);
        bufferConstrutivo.println("Insercao Rapida: " + pesoIR);
        bufferConstrutivo.close();

        //Execução dos algoritmos melhorativos     
        System.out.println("\n-------------- Melhorativo --------------");
        System.out.println("\nVizinho Proximo + 2OPT: ");   
        melhorativo2OPT(saidaVP,criaTabela("tabelaVP-2OPT",entrada),resultado.get(entrada));      
        System.out.println("\nVizinho Proximo + 3OPT: ");
        melhorativo3OPT(saidaVP,criaTabela("tabelaVP-3OPT",entrada),resultado.get(entrada));
        System.out.println("\nInsercao Rapida + 2OPT: ");
        melhorativo2OPT(saidaIR,criaTabela("tabelaIR-2OPT",entrada),resultado.get(entrada));
        System.out.println("\nInsercao Rapida + 3OPT: ");
        melhorativo3OPT(saidaIR,criaTabela("tabelaIR-3OPT",entrada),resultado.get(entrada));
    }
}
